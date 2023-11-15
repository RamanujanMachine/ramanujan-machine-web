import { parse } from 'mathjs';
import React from 'react';

function PolynomialInput({ numerator = false }: { numerator?: boolean }) {
	const [polynomial, setPolynomial] = React.useState('');
	const [polyClass, setPolyClass] = React.useState('form-field');

	let validatePolynomial = function () {
		try {
			let a = parse(polynomial);
			a.compile();
			setPolyClass('form-field');
		} catch (e) {
			console.log(e);
			setPolyClass('form-field invalid');
		}
	};

	return (
		<div className={polyClass}>
			<label>
				<i>{numerator ? 'p' : 'q'}</i>{' '}
			</label>
			<input
				value={polynomial}
				onChange={(event) => {
					setPolynomial(event.target.value);
				}}
				placeholder="enter a polynomial"
				onBlur={validatePolynomial}
			/>
		</div>
	);
}

export default PolynomialInput;
