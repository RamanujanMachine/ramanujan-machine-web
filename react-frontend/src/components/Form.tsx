import axios from 'axios';
import React, { useEffect, useState } from 'react';
import PolynomialInput from './PolynomialInput';
import Charts from './Charts';

interface PostBody {
	p: string;
	q: string;
	symbol: string | undefined;
	i: number;
}

function Form() {
	const [iterationCount, setIterationCount] = useState(1000);
	const [numeratorIsValid, setNumeratorValidity] = useState(false);
	const [denominatorIsValid, setDenominatorValidity] = useState(false);
	const [polynomialA, setPolynomialA] = useState('');
	const [polynomialB, setPolynomialB] = useState('');
	const [results, setResults] = useState<number[]>([]);
	const [showCharts, setShowCharts] = useState(false);

	useEffect(() => {
		document.getElementsByTagName('input')[0].focus();
	}, []);

	const onlyOneSymbolUsed = function () {
		const matches = (polynomialA + polynomialB).matchAll(/([a-zA-Z])/g);
		const distinctCharacters = new Set();
		for (const match of matches) {
			distinctCharacters.add(match[0]);
		}
		return distinctCharacters.size <= 1;
	};

	const errorClassFn = () => {
		return `error-message ${onlyOneSymbolUsed() ? 'hidden' : ''}`;
	};

	const formClassFn = () => {
		return `form ${
			numeratorIsValid && denominatorIsValid && onlyOneSymbolUsed() ? '' : 'invalid'
		} ${showCharts ? 'hidden' : ''}`;
	};

	const validateIterations = function (iterations: number) {
		if (iterations > 10000 || iterations <= 0) {
			setIterationCount(10000);
		} else setIterationCount(iterations);
	};

	const submit = (e: any) => {
		e.preventDefault();
		const body: PostBody = {
			p: polynomialA,
			q: polynomialB,
			symbol: polynomialA.match(/([a-zA-Z])/)?.[0] ?? polynomialB.match(/([a-zA-Z])/)?.[0],
			i: iterationCount
		};
		axios
			.post('http://localhost:8000/analyze', body)
			.then((response) => {
				if (response.status == 200) {
					setResults(response.data);
					setShowCharts(true);
				} else {
					setShowCharts(false);
					console.warn(response.data.error);
				}
			})
			.catch((error) => console.log(error.toJSON()));
	};

	return (
		<div>
			<form className={formClassFn()} onSubmit={submit}>
				<div>
					<p>
						Welcome to the Ramanujan Machine Polynomial Continued Fraction Explorer. Please enter
						the a
						<sub>
							<i>n</i>
						</sub>{' '}
						and b
						<sub>
							<i>n</i>
						</sub>{' '}
						polynomials below. They will define a continued fraction of the form:
					</p>
					<img src="pcf.png" alt="polynomial continued fraction template pretty printed" />
					<p>
						Which will then be calculated up to depth <i>n</i>.
					</p>

					<PolynomialInput
						numerator={true}
						updateFormValidity={(fieldValidity: boolean) => {
							setNumeratorValidity(fieldValidity);
						}}
						updatePolynomial={(polynomial: string) => {
							setPolynomialA(polynomial);
						}}></PolynomialInput>
					<PolynomialInput
						updateFormValidity={(fieldValidity: boolean) => {
							setDenominatorValidity(fieldValidity);
						}}
						updatePolynomial={(polynomial: string) => {
							setPolynomialB(polynomial);
						}}></PolynomialInput>
					<div className={errorClassFn()}>Please limit your polynomials to one variable</div>
					<div className="form-field">
						<div>
							<label>&nbsp;n&nbsp;</label>
						</div>
						<div>
							<input
								type="number"
								value={iterationCount}
								onChange={(event) => {
									validateIterations(Number(event.target.value));
								}}
							/>
						</div>
					</div>
					<button>Analyze</button>
				</div>
			</form>
			{showCharts ? (
				<Charts
					results={results}
					toggleDisplay={() => {
						setShowCharts(!showCharts);
					}}></Charts>
			) : null}
		</div>
	);
}

export default Form;
