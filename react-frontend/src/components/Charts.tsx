import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { MathJax, MathJaxContext } from 'better-react-mathjax';
import {parse} from 'mathjs';
import ScatterPlot from './ScatterPlot';
import constants from '../lib/constants';

interface ChartProps {
	results: any;
	toggleDisplay: () => void;
}

type WolframResult = {
	plaintext: string,
	title: string
}

function Charts({ results = {}, toggleDisplay }: ChartProps) {
	
    const [wolframResults, setWolframResults] = useState<WolframResult[]>();
    const config = {
        tex: {
            inlineMath: [["$", "$"]],
            displayMath: [["$$", "$$"]]
        }
    };

    useEffect(() => {
        verify();
    }, [results]);
  
    const computeValue = () => {
        // we are replacing the exponent operator from python to js syntax
        // we are also replacing the parentheses with the precision at the end of the expression returned from identify
        const input = convertConstants(JSON.parse(results.converges_to)
            .replaceAll('**','^')
            .replace(' = 0','')
            .replace(/\s\([0-9]+\)$/,'')
        );

        try { 
            const mathy = parse(input).toTex();
            return `$$${mathy}$$`;
        } catch(e) {
            console.log(`failed to parse ${input}`);
        }
    };

    const convertConstants = (input: string) => {
        let cleanString = input;
        for(const c in constants){
            if(constants[c].replacement) cleanString = cleanString.replaceAll(c, constants[c].replacement!!);
        }
        return cleanString;
    };

    const wolframValue = (input: string) => {
        if(input.indexOf('near') > -1) return;
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
        } catch(e) {
            console.log(`failed to parse ${cleanInput}`);
        }
    };

    const trimLimit = () => {
        const decimalPosition = results.limit.indexOf('.');
        return JSON.parse(results.limit).substring(0, 30 + decimalPosition + 1);
    };

    const computePairs = (dataset: string) => {
        return JSON.parse(results[dataset]);
    };

    const verify = () => {
        axios.post('/verify', {expression: results.limit})
            .then((response) => {
                if (response.status != 200) {
                    console.warn(response.data.error);
                }
                setWolframResults(response.data.wolfram_says);
            })
            .catch((error) => console.log(error));
    }

    return (
        <div className="chart-container">
            <MathJaxContext config={config} src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
                <div>
                    <p>This is the value of the Polynomial Continued Fraction:</p>
                    <div className="limit-container"><p className="center-text">{trimLimit()}</p></div>
                    <p className="footnote">
                        <i>
                    Note: the limit is estimated to high confidence using a PSLQ algorithm, but this is not a proof.
                        </i>
                    </p>
                </div>
                <div className="full-width top-padding">
                    <p className="center-content">It seems to converge to:</p>
                    <div className="closed-form-container">
                        <div className="closed-form">
                            <MathJax inline dynamic>{computeValue()}</MathJax>
                        </div>
                        {wolframResults?.map((r:WolframResult) => (
                            <div className="closed-form" key={r.plaintext}>
                                <p><MathJax inline dynamic>{wolframValue(r.plaintext)}</MathJax></p>
                            </div>
                        ))}
                    </div>
                </div>
            </MathJaxContext>
            <div className="top-padding">
                <p>The rate of convergence for this Polynomial Continued Fraction (in digits per step): </p>
                <ScatterPlot id="error_chart" data={computePairs('error_deriv')} />
            </div>
            <div className="top-padding">
                <p>
				Delta is a measure of the irrationality of a number (read more about it{' '}
                    <a href="https://www.ramanujanmachine.com/the-mathematics-of-polynomial-continued-fractions/irrationality-testing/">
					here
                    </a>
				). The given Polynomial Continued Fraction produces the following finite-depth estimations
				for Delta:
                </p>
                <ScatterPlot id="delta_chart" data={computePairs('delta')} />
            </div>
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
