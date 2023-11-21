import { parse } from 'mathjs';
import React from 'react';

function PolynomialInput({ numerator = false, updateFormValidity }: { numerator?: boolean, updateFormValidity: (fieldValidity: boolean)=> void }) {
	const [polynomial, setPolynomial] = React.useState('');
	const [polyClass, setPolyClass] = React.useState('form-field');

	const validatePolynomial = function () {
		if(polynomial.length == 0){
			setPolyClass('form-field invalid');
			updateFormValidity(false);
		} else {
		try {
			let a = parse(polynomial);
			a.compile();
			setPolyClass('form-field');
			updateFormValidity(true);
		} catch (e) {
			console.log(e);
			setPolyClass('form-field invalid');
			updateFormValidity(false);
		}}
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
					validatePolynomial();
				}}
				placeholder="enter a polynomial"
			/>
		</div>
	);
}

export default PolynomialInput;
