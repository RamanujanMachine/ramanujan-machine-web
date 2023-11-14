import React, { useEffect } from 'react';
import PolynomialInput from './PolynomialInput';

function Form() {
	const [iterationCount, setIterationCount] = React.useState(1000);

	let validateIterations = function (iterations: number) {
		if (iterationCount > 10000) {
			setIterationCount(10000);
		}
	};

	useEffect(() => {
		document.getElementsByTagName('input')[0].focus();
	}, []);

	return (
		<div>
			<div className="form">
				<p>
					This is some temporary copy pulled from the web site. The simple continued fraction
					expansion is an intriguing way of writing real numbers, which holds within it many
					interesting properties of the number itself. These continued fractions have a remarkable
					tendency to emerge in various places.{' '}
				</p>

				<PolynomialInput numerator={true}></PolynomialInput>
				<PolynomialInput></PolynomialInput>
				<div className="form-field">
					<div>
						<label>iterations</label>
					</div>
					<div>
						<input
							type="number"
							value={iterationCount}
							onChange={(event) => {
								setIterationCount(Number(event.target.value));
							}}
							onBlur={(event) => {
								validateIterations(Number(event.target.value));
							}}
						/>
					</div>
				</div>
				<button>Analyze</button>
			</div>
		</div>
	);
}

export default Form;
