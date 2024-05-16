import React, { useEffect, useState } from 'react';
import PolynomialInput from './PolynomialInput';
import Charts from './Charts';
import { CoordinatePair } from '../lib/types';

interface PostBody {
	a: string;
	b: string;
	symbol: string | undefined;
	i: number;
	precision?: number;
}
 
function Form() {
	const [iterationCount, setIterationCount] = useState(1000);
	const [numeratorIsValid, setNumeratorValidity] = useState(false);
	const [denominatorIsValid, setDenominatorValidity] = useState(false);
	const [polynomialA, setPolynomialA] = useState('');
	const [polynomialB, setPolynomialB] = useState('');
	const [showCharts, setShowCharts] = useState(false);
	const [noConvergence, setNoConvergence] = useState(false);
	const [waitingForResponse, setWaitingForResponse] = useState(false);
	const [convergesTo, setConvergesTo] = useState([]);
	const [limit, setLimit] = useState('');
	const [deltaData, setDeltaData] = useState<CoordinatePair[]>([]);

	useEffect(() => {
		document.getElementsByTagName('input')[0].focus();
	}, []);

	const resetState = function () {
		setConvergesTo([]);
		setLimit('');
		setDeltaData([]);
	};

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

	const spinnerClassFn = () => {
		return `spinner ${waitingForResponse ? '' : 'hidden'}`;
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

	const isolateSymbol = () => {
		return polynomialA.match(/([a-zA-Z])/)?.[0] ?? polynomialB.match(/([a-zA-Z])/)?.[0] ?? '';
	}

	const submit = (e: any) => {
		e.preventDefault();
		setWaitingForResponse(true);
		setNoConvergence(false);

		let websocket = new WebSocket('ws://127.0.0.1:80/data');

		websocket.onopen = () => {
			console.log('socket connection opened');

			const body: PostBody = {
				a: polynomialA,
				b: polynomialB,
				symbol: isolateSymbol(),
				i: iterationCount
			};

			websocket.send(JSON.stringify(body));
			setWaitingForResponse(true);
		};

		websocket.onerror = (e) => {
			console.log('web socket error', e);
		};

		websocket.onclose = () => {
			console.log('web socket closed');
		};

		websocket.onmessage = (evt) => {
			setWaitingForResponse(false);
			const message = JSON.parse(evt.data);
			if (Object.hasOwn(message, 'limit')) {
				setShowCharts(true);
				setLimit(message.limit);
			}
			if (Object.hasOwn(message, 'is_convergent')) {
				if (message.is_convergent !== false) {
					setShowCharts(true);
				} else if (message.is_convergent === false) {
					setNoConvergence(true);
					websocket.close();
					return;
				}
			} else if (Object.hasOwn(message, 'converges_to')) {
				setConvergesTo(JSON.parse(message.converges_to));
			} else if (Object.hasOwn(message, 'delta')) {
				const incomingDeltaData = JSON.parse(message.delta);
				if (incomingDeltaData.length > 0) {
					setDeltaData((previousData) => [...previousData, ...incomingDeltaData]);
				}
			}
		};
	};

	return (
		<div className="form-parent">
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
					<div className="image-parent">
						<img src="/form/pcf.png" alt="polynomial continued fraction template pretty printed" />
					</div>
					<p>
						Which will then be calculated up to depth <i>n</i>.
					</p>

					<PolynomialInput
						numerator={true}
						updateFormValidity={(fieldValidity: boolean) => {
							setNoConvergence(false);
							setNumeratorValidity(fieldValidity);
						}}
						updatePolynomial={(polynomial: string) => {
							setNoConvergence(false);
							setPolynomialA(polynomial);
						}}></PolynomialInput>
					<PolynomialInput
						updateFormValidity={(fieldValidity: boolean) => {
							setNoConvergence(false);
							setDenominatorValidity(fieldValidity);
						}}
						updatePolynomial={(polynomial: string) => {
							setNoConvergence(false);
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
					<button>
						<div className={spinnerClassFn()}></div>
						<div className="button-text">Analyze</div>
					</button>
				</div>
			</form>
			{noConvergence ? <h3>The provided polynomials do not converge.</h3> : null}
			{showCharts ? (
				<Charts
					a_n={polynomialA}
					b_n={polynomialB}
					limit={limit}
					symbol={isolateSymbol()}
					convergesTo={convergesTo}
					deltaData={deltaData}
					toggleDisplay={() => {
						setNoConvergence(false);
						setShowCharts(!showCharts);
						resetState();
					}}></Charts>
			) : null}
		</div>
	);
}

export default Form;
