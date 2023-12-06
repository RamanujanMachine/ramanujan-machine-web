/* eslint-disable no-unused-vars */
import { parse } from 'mathjs';
import React from 'react';

interface PolynomialInputProps {
	numerator?: boolean;
	updateFormValidity: (isValid: boolean) => void;
	updatePolynomial: (polynomial: string) => void;
}

function PolynomialInput({
	numerator = false,
	updateFormValidity,
	updatePolynomial
}: PolynomialInputProps) {
	const [localPoly, setLocalPoly] = React.useState('');
	const [polyClass, setPolyClass] = React.useState('form-field');
	const [errorMessage, setErrorMessage] = React.useState('');
	const [errorClass, setErrorClass] = React.useState('error-message hidden');

	const MAX_INPUT_LENGTH = 100;

	const valid = function () {
		setErrorClass('error-message hidden');
		setPolyClass('form-field');
		updateFormValidity(true);
	};

	const invalid = function () {
		setErrorClass('error-message fade-in');
		setPolyClass('form-field invalid');
		updateFormValidity(false);
	};

	const sanitize = function (input: string) {
		// replace all characters that are not valid math expression characters
		return input.replaceAll(/[^^()a-zA-Z0-9*./ +-]*/g, '');
	};

	const validatePolynomial = function (p: string) {
		if (p.length == 0) {
			invalid();
			setErrorMessage('A value is required');
			setLocalPoly(p);
		} else if (p.length > MAX_INPUT_LENGTH) {
			setLocalPoly(p.substring(0, MAX_INPUT_LENGTH));
		} else {
			let clean = sanitize(p);
			if (clean !== p) {
				setLocalPoly(clean);
			} else {
				setLocalPoly(p);
				try {
					parse(p);
					setErrorMessage('');
					valid();
				} catch (e) {
					setErrorMessage(e!.toString());
					invalid();
				}
			}
		}
	};

	return (
		<div>
			<div className={polyClass}>
				<label>
					<i>{numerator ? 'p' : 'q'}</i>{' '}
				</label>
				<input
					value={localPoly}
					onChange={(event) => {
						validatePolynomial(event.target.value);
					}}
					onBlur={() => {
						updatePolynomial(localPoly);
					}}
					placeholder="enter a polynomial"
				/>
			</div>
			<div className={errorClass}>{errorMessage}</div>
		</div>
	);
}

export default PolynomialInput;
