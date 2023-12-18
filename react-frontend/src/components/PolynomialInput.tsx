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
		setErrorMessage('');
		setErrorClass('error-message hidden');
		setPolyClass('form-field');
		updateFormValidity(true);
	};

	const invalid = function (errorMessage = '') {
		setErrorMessage(errorMessage);
		setErrorClass('error-message fade-in');
		setPolyClass('form-field invalid');
		updateFormValidity(false);
	};

	const sanitize = function (input: string) {
		// replace all characters that are not valid math expression characters
		return input.replaceAll(/[^^()a-zA-Z0-9*./ +-]*/g, '');
	};

	const onlyOneSymbol = function (input: string) {
		const matches = input.matchAll(/([a-zA-Z])/g);
		const distinctCharacters = new Set();
		for (const match of matches) {
			distinctCharacters.add(match[0]);
		}
		return distinctCharacters.size <= 1;
	};

	const validatePolynomial = function (p: string) {
		if (p.length == 0) {
			// validate non-empty
			invalid('A value is required');
			setLocalPoly(p);
		} else if (p.length > MAX_INPUT_LENGTH) {
			// validate length
			setLocalPoly(p.substring(0, MAX_INPUT_LENGTH));
		} else if (!onlyOneSymbol(p)) {
			// validate that there is only one variable in use
			invalid('Please limit to one variable');
			setLocalPoly(p);
		} else {
			// strip extraneous special characters
			let clean = sanitize(p);
			if (clean !== p) {
				setLocalPoly(clean);
			} else {
				setLocalPoly(p);
				try {
					parse(p);
					valid();
				} catch (e) {
					invalid(e!.toString());
				}
			}
		}
	};

	return (
		<div>
			<div className={polyClass}>
				<label>
					{numerator ? 'a' : 'b'}
					<sub>n</sub>
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
