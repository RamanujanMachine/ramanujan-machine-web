import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { MathJax, MathJaxContext } from 'better-react-mathjax';
import { parse } from 'mathjs';
import ScatterPlot from './ScatterPlot';
import constants from '../lib/constants';
import { CoordinatePair } from '../lib/types';

interface ChartProps {
	a_n: string;
	b_n: string;
	limit?: string;
	symbol: string;
	convergesTo?: string[];
	seeAlso?: string[];
	deltaData?: CoordinatePair[];
	toggleDisplay: () => void;
}

type WolframResult = {
	plaintext: string;
	title: string;
	description: string;
	link: string;
};

type WolframLink = {
	url: string;
};

type WolframMetadata = {
	text: string;
	links: WolframLink | WolframLink[];
};

type ConstantMetadata = {
	name: string;
	url?: string;
};

type ConstantMetadataWrapper = {
	[key: string]: ConstantMetadata;
};

function Charts({ a_n, b_n, limit, symbol, convergesTo, seeAlso, deltaData, toggleDisplay }: ChartProps) {
	const [wolframResults, setWolframResults] = useState<WolframResult[]>();
	const [constantMetadata, setConstantMetadata] = useState<Record<string, ConstantMetadata>>({});
	const [lirecClosedForm, setLirecClosedForm] = useState<string[]>();
	const [seeAlsoClosedForm, setSeeAlsoClosedForm] = useState<string[][]>();
	const [pcf, setPcf] = useState('');

	// MathJax config
	const config = {
		tex: {
			inlineMath: [['$', '$']],
			displayMath: [['$$', '$$']]
		}
	};

	useEffect(() => {
		if (limit) verify();
	}, [limit]);

	useEffect(() => {
		if (Array.isArray(seeAlso) && seeAlso.length > 0) {
			setSeeAlsoClosedForm(restructureSeeAlso(seeAlso));
		}
	}, [seeAlso]);

	useEffect(() => {
		if (Array.isArray(convergesTo) && convergesTo.length > 0) {
			setLirecClosedForm(replaceLirecChars(convergesTo));
		}
	}, [convergesTo]);

	const wrapExpression = (input: string, label?: string) => {
		const expr = label ? label.concat(' = ', input) : input;
		let parsed, mathy;
		try {
			parsed = parse(expr);
			mathy = parsed.toTex({ parenthesis: 'auto' });
			return `$$${mathy}$$`;
		} catch (e) {
			console.error(`failed to parse ${input}`);
			return `$$${input}$$`;
		}
	};

	let formatPcf = function(_a_n: string, _b_n:string) {
		// preset to input value
		console.log('format inputs' ,_a_n, _b_n);
		let a = _a_n.replaceAll('**','^');
		console.log('a', a);
		let a_parsed = parse(a);
		console.log('a parsed', a_parsed);
		let b = _b_n.replaceAll('**','^');
		console.log('b', b);
		let b_parsed = parse(b);
		console.log('b parsed', b_parsed);
		let [a0, a1, a2] = [a_parsed.evaluate({n: 0}), a_parsed.evaluate({n: 1}), a_parsed.evaluate({n: 2})];
		console.log('a0',a0, 'a1',a1,'a2',a2);
		let [b1_eval, b2_eval, b3_eval] = [b_parsed.evaluate({n: 1}),b_parsed.evaluate({n: 2}),b_parsed.evaluate({n: 3})];
		let [,b1_sign, b2_sign, b3_sign] = [undefined, b1_eval > 0 ? '+': '-',b2_eval > 0 ? '+': '-',b3_eval > 0 ? '+': '-'];
		console.log('b signs', b1_sign, b2_sign, b3_sign);
		let parsed = parse(`${a0} ${b1_sign} (${b1_eval} / (${a1} ${b2_sign} (${b2_eval} / (${a2} ${b3_sign} (${b3_eval} / (dots + ${b} / (${a} + dots)))))))`);
		console.log('parsed', parsed);
		let mathy = parsed.toTex({ parenthesis: 'auto' });
		// this is a hack because mathjs chokes on the dots so we put them in after the expression is Texed
		return `$$${mathy.replaceAll('dots', '...')}$$`;
	}

	useEffect(() => {
		setPcf(formatPcf(a_n, b_n));
	}, [a_n, b_n, symbol]);

	const restructureSeeAlso = (input: string[]) => {
		let result = new Array<string[]>();
		for (const value of input!!) {
			console.log('input',value);
			const cleanString = value
				.replaceAll('PCF[','')
				.replaceAll('] =', '=')
				.replaceAll('**', '^')
				.replace(/\s\(-?[0-9]+\)$/, '');
			console.log('clean', cleanString);
			const input = convertLirecConstants(cleanString);
			console.log('converted', input);
			let [pcf_a, remnant] = input.split(',');
			console.log('pcf_a', pcf_a, 'remnant', remnant);
			let [pcf_b, exp] = remnant.split('=');
			console.log('pcf_b', pcf_b, 'exp', exp);
			console.log('wrapped pcf', formatPcf(pcf_a, pcf_b));
			console.log('wrapped exp', wrapExpression(exp));
			result.push([wrapExpression(exp), formatPcf(pcf_a, pcf_b)]);
		}
		return result;
	};

	const replaceLirecChars = (input: string[]) => {
		// we are replacing the exponent operator from python to js syntax
		// we are also stripping the parentheses at the end of the expression returned from identify
		let result = new Array<string>();
		for (const value of input!!) {
			const cleanString = value
				.replaceAll('**', '^')
				.replace(' = 0', '')
				.replace(/\s\(-?[0-9]+\)$/, '');
			const input = convertLirecConstants(cleanString);
			result.push(wrapExpression(input));
		}
		return result;
	};

	// e.g. '(20*alpha_GW - 34)/(alpha_GW + 9)'
	// should convert to '(20*α[GW] - 34)/(α[GW] + 9)'
	const convertLirecConstants = (input: string) => {
		let cleanString = input;
		for (const c in constants) {
			// make sure it's not a substring of another constant name by checking that the constant name
			// we are processing is either surrounded by non-constant characters or at the beginning/end of the string
			const tightPattern = new RegExp(`(^|\\W+|\\[[^\\]]*\\])${c}(\\W+|\\[[^\\]]*\\]|$)`);
			if (tightPattern.test(cleanString)) {
				if (constants[c].replacement) {
					cleanString = cleanString.replaceAll(c, constants[c].replacement!!);
				}
				let name = `${constants[c].replacement ? constants[c].replacement!! : c!!} is the ${constants[c].name!!}`;
				if (constants[c].name || constants[c].url) {
					let meta: ConstantMetadata = {
						name: name
					};
					if (constants[c].url) {
						meta.url = constants[c].url!!;
					}
					let newObj: ConstantMetadataWrapper = {};
					newObj[meta.name] = meta;
					setConstantMetadata((previousMetadata) =>
						Object.hasOwn(previousMetadata, name)
							? { ...previousMetadata, ...newObj }
							: previousMetadata
					);
				}
			}
		}
		return cleanString;
	};

	const wolframValue = (input: string) => {
		if (input.indexOf('near') > -1) return;
		// wolfram regurgitates the value provided with an approx symbol - truncating
		let cleanInput = input.indexOf('≈') >= 0 ? input.substring(0, input.indexOf('≈')) : input;
		// replace root of if it wraps a sub expression in parens first since it's a more specific match
		if (cleanInput.indexOf('root of (') > -1) {
			cleanInput = cleanInput.replace(/root\sof\s\(([^)]+)\)(.*)/g, 'sqrt($1)$2');
		}
		// then go after the entire expression
		if (cleanInput.indexOf('root of ') > -1) {
			cleanInput = cleanInput.replace(/root\sof\s(.*)/g, 'sqrt($1)');
		}
		cleanInput = wolframTextCleanup(cleanInput);
		try {
			const mathy = parse(cleanInput).toTex();
			return `$$${mathy}$$`;
		} catch (e) {
			console.error(`failed to parse ${cleanInput}`);
		}
	};

	// were having issues with underscores not properly converting the subsequent text to subscript,
	// this fixes that bug
	const wolframTextCleanup = (input: string) => {
		let text = input;
		if (text.indexOf('_') > -1) {
			text = text.replace(/_([a-zA-Z]+)/, '[' + '$1' + '] ');
		}
		if (text.indexOf("'s") > -1) {
			// traditional apostrophe gets replaced with superscript H
			text = text.replace("'s", 's');
		}
		return text;
	};

	// we get constant/symbol metadata from both wolfram and LIReC and we need to consolidate into
	// a unified format to prevent duplicates and line up the attribute names
	const polishMetadata = (input: WolframMetadata) => {
		let name = wolframTextCleanup(input.text);
		const newMeta = {
			name: name,
			url: Array.isArray(input.links) ? input.links[0].url : input.links?.url
		};
		let newObj: ConstantMetadataWrapper = {};
		newObj[input.text] = newMeta;
		setConstantMetadata((previousMetadata) => ({ ...previousMetadata, ...newObj }));
	};

	const verify = () => {
		if (limit) {
			axios.post('/verify', { expression: limit })
				.then((response) => {
					if (response.status != 200) {
						console.warn(response.data.error);
					}
					// keys are "closed_forms" and "metadata" where metadata has entries of the form: ["text": "", "links": {"url":"...", ...}]
					// "links" can also be an array of objects
					let wolframData = response.data.wolfram_says.closed_forms;
					// add link from metadata if present
					// add description from metadata if present
					setWolframResults(wolframData);
					if (typeof response.data.wolfram_says.metadata != 'undefined') {
						if (Array.isArray(response.data.wolfram_says.metadata)) {
							for (let m of response.data.wolfram_says.metadata) {
								polishMetadata(m);
							}
						} else {
							polishMetadata(response.data.wolfram_says.metadata);
						}
					}
				})
				.catch((error) => console.log(error));
		}
	};

	return (
		<div className="chart-container">
			<p className="nav-wrapper">
				<a
					target="_self"
					onClick={() => {
						toggleDisplay();
					}}>
					&larr;&nbsp;back to form
				</a>
			</p>
			<MathJaxContext config={config} src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
				<div className="flex-wrapper">
					<div className="flex-child">
						<p>
							<MathJax inline dynamic>
								{pcf}
							</MathJax>
						</p>
					</div>
				</div>
				{limit ? (
					<div>
						<p>This is the value of the Polynomial Continued Fraction:</p>
						<div className="limit-container">
							<p className="center-text">{limit}</p>
						</div>
						<p className="footnote">
							<i>
								Note: the limit is estimated to high confidence using a PSLQ algorithm, but this is
								not a proof.
							</i>
						</p>
					</div>
				) : (
					''
				)}
				{convergesTo ? (
					<div className="full-width top-padding">
						<p className="center-content">It seems to converge to</p>
						<div className="top-padding center-text">
							<p className="footnote">
								<i>
									Results from{' '}
									<a
										href="https://github.com/RamanujanMachine/LIReC"
										aria-description="Link to LIReC GitHub repository README.">
										LIReC
									</a>
								</i>
							</p>
						</div>
						<div className="closed-form-container">
							<div className="closed-form">
								<MathJax inline dynamic>
									{lirecClosedForm}
								</MathJax>
							</div>
						</div>
						{wolframResults ? (
							<div className="top-padding center-text">
								<p className="footnote">
									<i>
										Results from{' '}
										<a
											href="https://www.wolframalpha.com/"
											aria-description="Link to WolframAlpha web interface.">
											WolframAlpha
										</a>
									</i>
								</p>
							</div>
						) : (
							''
						)}
						<div className="closed-form-container">
							{wolframResults?.map((r: WolframResult) =>
								wolframValue(r.plaintext) ? (
									<div className="closed-form" key={r.plaintext}>
										<p>
											<MathJax inline dynamic>
												{wolframValue(r.plaintext)}
											</MathJax>
										</p>
									</div>
								) : (
									''
								)
							)}
						</div>
						<div className="meta-container">
							<div>
								{constantMetadata
									? Object.values(constantMetadata).map((entry: ConstantMetadata) => (
										<p className="footnote metadata" key={entry.name}>
											<MathJax inline dynamic>
												{wrapExpression(entry.name)}
											</MathJax>
											{typeof entry.url != 'undefined' ? (
												<a className="metadata" href={entry.url} target="_blank" rel="noreferrer">
													&nbsp;&#x1F517;
												</a>
											) : (
												''
											)}
										</p>
									))
									: ''}
							</div>
						</div>
					</div>
				) : (
					''
				)}
				{seeAlso ? (
					<div className="full-width top-padding">
						<p className="center-content">See also</p>
						<div className="top-padding center-text">
							<p className="footnote">
								<i>
									Results from{' '}
									<a
										href="https://github.com/RamanujanMachine/LIReC"
										aria-description="Link to LIReC GitHub repository README.">
										LIReC
									</a>
								</i>
							</p>
						</div>
						<div className="closed-form-container">
							{seeAlsoClosedForm?.map((pcf: string[]) =>
								(<div className="closed-form" key={pcf[0]}>
									<MathJax inline dynamic>
										{pcf[0]}
									</MathJax>
									<span className="align-self-center">=</span>
									<MathJax inline dynamic>
										{pcf[1]}
									</MathJax>
								</div>)
							)}
						</div>
					</div>
				) : (
					''
				)}
				{deltaData && deltaData?.length > 0 ? (
					<div className="top-padding plot-container">
						<p>
							Delta is a measure of the irrationality of a number (read more about it{' '}
							<a href="https://www.ramanujanmachine.com/the-mathematics-of-polynomial-continued-fractions/irrationality-testing/">
								here
							</a>
							). The given Polynomial Continued Fraction produces the following finite-depth
							estimations for Delta:
						</p>
						<ScatterPlot id="delta_chart" data={deltaData} />
					</div>
				) : (
					''
				)}
			</MathJaxContext>
			<button
				onClick={() => {
					toggleDisplay();
				}}>
				Modify Inputs
			</button>
		</div>
	);
}

export default Charts;
