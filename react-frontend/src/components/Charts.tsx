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
	convergesTo?: string;
	errorData?: CoordinatePair[];
	deltaData?: CoordinatePair[];
	reducedDeltaData?: CoordinatePair[];
	toggleDisplay: () => void;
}

type WolframResult = {
	plaintext: string;
	title: string;
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
	const config = {
		tex: {
			inlineMath: [['$', '$']],
			displayMath: [['$$', '$$']]
		}
	};

	useEffect(() => {
		if (limit) verify();
	}, [limit]);

	const wrapExpression = (input: string, label?: string) => {
		try {
			const mathy = parse(label ? label.concat(' = ', input) : input).toTex();
			return `$$${mathy}$$`;
		} catch (e) {
			console.log(`failed to parse ${input}`);
		}
	};

	const computeValue = () => {
		// we are replacing the exponent operator from python to js syntax
		// we are also replacing the parentheses with the precision at the end of the expression returned from identify
		if (convergesTo) {
			const input = convertConstants(
				convergesTo
					.replaceAll('**', '^')
					.replace(' = 0', '')
					.replace(/\s\([0-9]+\)$/, '')
			);

			return wrapExpression(input);
		}
	};

	const convertConstants = (input: string) => {
		let cleanString = input;
		for (const c in constants) {
			if (constants[c].replacement)
				cleanString = cleanString.replaceAll(c, constants[c].replacement!!);
		}
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
					setWolframResults(response.data.wolfram_says);
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
									{computeValue()}
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
