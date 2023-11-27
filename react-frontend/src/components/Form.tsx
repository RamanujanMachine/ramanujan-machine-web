import axios from 'axios';
import React, { useEffect } from 'react';
import PolynomialInput from './PolynomialInput';

function Form() {
	const [iterationCount, setIterationCount] = React.useState(1000);
	const [numeratorIsValid, setNumeratorValidity] = React.useState(false);
	const [denominatorIsValid, setDenominatorValidity] = React.useState(false);
	const [polynomialA, setPolynomialA] = React.useState('');
	const [polynomialB, setPolynomialB] = React.useState('');

	useEffect(() => {
		document.getElementsByTagName('input')[0].focus();
	}, []);

	const formClassFn = () => {
		return `form ${numeratorIsValid && denominatorIsValid ? '' : 'invalid'}`;
	};

	const validateIterations = function (iterations: number) {
		if (iterations > 10000 || iterations <= 0) {
			setIterationCount(10000);
		} else setIterationCount(iterations);
	};

	const submit = (e: any) => {
		e.preventDefault();
		axios
			.post('http://localhost:8000/analyze', {
				p: polynomialA,
				q: polynomialB,
				i: iterationCount
			})
			.then((response) => {
				console.log('submitted', response);
			})
			.catch((error) => console.log(error));
	};

	return (
		<form className={formClassFn()} onSubmit={submit}>
			<div>
				<p>
					Welcome to the Ramanujan Machine Polynomial Continued Fraction Explorer. Please enter the
					a
					<sub>
						<i>n</i>
					</sub>{' '}
					and b
					<sub>
						<i>n</i>
					</sub>{' '}
					polynomials below. They will define a continued fraction of the form:
				</p>
				<img src="pcf.svg" alt="polynomial continued fraction template pretty printed" />
				<p>
					Which will then be calculated up to depth <i>n</i>.
				</p>

				<PolynomialInput
					numerator={true}
					updateFormValidity={(fieldValidity: boolean) => setNumeratorValidity(fieldValidity)}
					updatePolynomial={(polynomial: string) => {
						setPolynomialA(polynomial);
					}}></PolynomialInput>
				<PolynomialInput
					updateFormValidity={(fieldValidity: boolean) => setDenominatorValidity(fieldValidity)}
					updatePolynomial={(polynomial: string) => {
						setPolynomialB(polynomial);
					}}></PolynomialInput>
				<div className="form-field">
					<div>
						<label>
							<i>n</i>
						</label>
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
	);
}

export default Form;
