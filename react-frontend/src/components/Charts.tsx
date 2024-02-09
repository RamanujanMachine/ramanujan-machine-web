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
	
    const [wolframResults, setWolframResults] = useState<WolframResult[]>([]);
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
            return '(unparseable result)';
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
        // wolfram regurgitates the value provided with an approx symbol - truncating
        const cleanInput = input.indexOf('≈') >= 0 ? input.substring(0, input.indexOf('≈')) : input;
        try { 
            const mathy = parse(cleanInput).toTex();
            return `$$${mathy}$$`;
        } catch(e) {
            console.log(`failed to parse ${cleanInput}`);
            return '(unparseable result)';
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
                <p>This is the value of the Polynomial Continued Fraction:</p>
                <p className="center-text">{trimLimit()}</p>
                <p>It seems to converge to:<br/><br/> <MathJax inline dynamic>{computeValue()}</MathJax></p>
                { wolframResults && wolframResults.length > 0 ? (
                    <div>
                        <p className="center-text"><i>or</i></p>
                        <p><MathJax inline dynamic>{wolframValue(wolframResults[0].plaintext)}</MathJax></p>
                    </div>
                ):''}
            </MathJaxContext>
            <i>
                <sub>
					Note: the limit is estimated to high confidence using a PSLQ algorithm, but this is not a
					proof.
                </sub>
            </i>
            <p>The rate of convergence for this Polynomial Continued Fraction (in digits per step): </p>
            <ScatterPlot id="error_chart" data={computePairs('error_deriv')} />
            <p>
				Delta is a measure of the irrationality of a number (read more about it{' '}
                <a href="https://www.ramanujanmachine.com/the-mathematics-of-polynomial-continued-fractions/irrationality-testing/">
					here
                </a>
				). The given Polynomial Continued Fraction produces the following finite-depth estimations
				for Delta:
            </p>
            <ScatterPlot id="delta_chart" data={computePairs('delta')} />
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
