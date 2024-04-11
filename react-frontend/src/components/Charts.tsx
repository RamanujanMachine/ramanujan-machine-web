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
	convergesTo?: string[];
	errorData?: CoordinatePair[];
	deltaData?: CoordinatePair[];
	reducedDeltaData?: CoordinatePair[];
	toggleDisplay: () => void;
}

type WolframResult = {
	plaintext: string;
	title: string;
	description: string;
	link: string;
};

type MetadataLink = {
	url: string;
	text: string;
	title: string;
};

type ConstantMetadata = {
	text: string;
	links: MetadataLink | MetadataLink[];
};

type LirecConstantMetadata = {
	label?: string;
	expression: string;
	url?: string;
};

function Charts({
	a_n,
	b_n,
	limit,
	convergesTo,
	errorData,
	deltaData,
	reducedDeltaData,
	toggleDisplay
}: ChartProps) {
	const [wolframResults, setWolframResults] = useState<WolframResult[]>();
	const [constantMetadata, setConstantMetadata] = useState<ConstantMetadata[]>([]);
	const [lirecConstantMetadata, setLirecConstantMetadata] = useState<LirecConstantMetadata[]>([]);
	const [lirecClosedForm, setLirecClosedForm] = useState<string[]>();
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
		if (Array.isArray(convergesTo) && convergesTo.length > 0) {
			setLirecClosedForm(replaceLirecChars());
		}
	}, [convergesTo]);

	const wrapExpression = (input: string, label?: string) => {
		const expr = label ? label.concat(' = ', input) : input;
		try {
			const mathy = parse(expr).toTex();
			return `$$${mathy}$$`;
		} catch (e) {
			console.log(`failed to parse ${input}`);
			return expr;
		}
	};

	const replaceLirecChars = () => {
		// we are replacing the exponent operator from python to js syntax
		// we are also replacing the parentheses with the precision at the end of the expression returned from identify
		let result = new Array<string>();
		for (const value of convergesTo!!) {
			const cleanString = value
				.replaceAll('**', '^')
				.replace(' = 0', '')
				.replace(/\s\([0-9]+\)$/, '');
			const input = convertLirecConstants(cleanString);
			result.push(wrapExpression(input));
		}
		return result;
	};
	// e.g. '(20*alpha_GW - 34)/(alpha_GW + 9)'
	// should convert to '(20*α[GW] - 34)/(α[GW] + 9)'
	const convertLirecConstants = (input: string) => {
		let constantMeta: LirecConstantMetadata[] = [];
		let cleanString = input;
		for (const c in constants) {
			// make sure it's not a substring of another constant name by checking that the constant name
			// we are processing is either surrounded by non-constant characters or at the beginning/end of the string
			const tightPattern = new RegExp(`(^|\\W+|\\[[^\\]]*\\])${c}(\\W+|\\[[^\\]]*\\]|$)`);
			if (tightPattern.test(cleanString)) {
				if (constants[c].replacement) {
					cleanString = cleanString.replaceAll(c, constants[c].replacement!!);
				}
				if (constants[c].name || constants[c].url) {
					let meta: LirecConstantMetadata = {
						expression: constants[c].replacement ? constants[c].replacement!! : c!!
					};
					if (constants[c].name) {
						meta.label = constants[c].name!!;
					}
					if (constants[c].url) {
						meta.url = constants[c].url!!;
					}
					constantMeta.push(meta);
				}
			}
		}
		setLirecConstantMetadata(constantMeta);
		return cleanString;
	};

	const wolframValue = (input: string) => {
		if (input.indexOf('near') > -1) return;
		// wolfram regurgitates the value provided with an approx symbol - truncating
		let cleanInput = input.indexOf('≈') >= 0 ? input.substring(0, input.indexOf('≈')) : input;
		// replace root of if it wraps a sub expression in parens first since it's a more specific match
		if (cleanInput.indexOf('root of (') > -1) {
			cleanInput.replace(/root\sof\s\(([^)]+)\)(.*)/g, 'sqrt($1)$2');
		}
		// then go after the entire expression
		if (cleanInput.indexOf('root of ') > -1) {
			cleanInput.replace(/root\sof\s(.*)/g, 'sqrt($1)');
		}
		if (cleanInput.indexOf('_') > -1) {
			cleanInput.replace(/_\(\w\)/, '[' + '$1' + ']');
		}
		try {
			const mathy = parse(cleanInput).toTex();
			return `$$${mathy}$$`;
		} catch (e) {
			console.log(`failed to parse ${cleanInput}`);
		}
	};

	const trimLimit = () => {
		if (limit) {
			const decimalPosition = limit.indexOf('.');
			return limit.substring(0, 30 + decimalPosition + 1);
		}
	};

	const verify = () => {
		if (limit) {
			axios
				.post('/verify', { expression: limit })
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
							if (response.data.wolfram_says.metadata.length > 0) {
								setConstantMetadata(response.data.wolfram_says.metadata);
							}
						} else {
							setConstantMetadata([response.data.wolfram_says.metadata]);
						}
					}
				})
				.catch((error) => console.log(error));
		}
	};

	return (
		<div className="chart-container">
			<MathJaxContext config={config} src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
				<div className="flex-wrapper">
					<div className="flex-child">
						<p>
							<MathJax inline dynamic>
								{wrapExpression(a_n, 'a[n]')}
							</MathJax>
						</p>
					</div>
					<div className="flex-child">
						<p>
							<MathJax inline dynamic>
								{wrapExpression(b_n, 'b[n]')}
							</MathJax>
						</p>
					</div>
				</div>
				{limit ? (
					<div>
						<p>This is the value of the Polynomial Continued Fraction:</p>
						<div className="limit-container">
							<p className="center-text">{trimLimit()}</p>
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
										LIReC identify()
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
						<div className="meta-container">
							{constantMetadata?.map((m: ConstantMetadata) => (
								<a
									className="metadata"
									href={Array.isArray(m.links) ? m.links[0].url : m.links?.url}
									key={m.text}>
									<MathJax inline dynamic>
										{wrapExpression(m.text)}
									</MathJax>
								</a>
							))}
							{lirecConstantMetadata?.map((l: LirecConstantMetadata) =>
								l.url ? (
									<a className="metadata" href={l.url} key={l.label}>
										<MathJax inline dynamic>
											{wrapExpression(l.expression)}
										</MathJax>
										is the {l.label}
									</a>
								) : (
									<p className="footnote metadata" key={l.label}>
										<MathJax inline dynamic>
											{wrapExpression(l.expression)}
										</MathJax>
										is the {l.label}
									</p>
								)
							)}
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
							{constantMetadata?.map((m: ConstantMetadata) => (
								<a
									className="metadata"
									href={Array.isArray(m.links) ? m.links[0].url : m.links?.url}
									key={m.text}>
									<MathJax inline dynamic>
										{wrapExpression(m.text)}
									</MathJax>
								</a>
							))}
						</div>
					</div>
				) : (
					''
				)}
				<div className="top-padding plot-container">
					<p>
						The rate of convergence for this Polynomial Continued Fraction (in digits per step):{' '}
					</p>
					<ScatterPlot id="error_chart" data={errorData} />
				</div>
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
					<ScatterPlot id="reduced_delta_chart" data={reducedDeltaData} />
				</div>
			</MathJaxContext>
			<button
				onClick={() => {
					toggleDisplay();
				}}>
				Modify
			</button>
		</div>
	);
}

export default Charts;
