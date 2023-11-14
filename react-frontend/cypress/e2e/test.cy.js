/// <reference types="cypress" />

describe('landing form', () => {
	beforeEach(() => {
		cy.visit('http://localhost:3000');
	});

	it('displays two input fields for polynomials and one for iterations', () => {
		cy.get('input').should('have.length', 3);
		cy.get('input').first().should('have.text', '');
		cy.get('input').eq(1).should('have.text', '');
		cy.get('input').eq(2).should('have.value', '1000');
	});

	it('should be focused on first input element', () => {
		cy.get('input').first().should('have.focus');
	});

	it('validates math expressions', () => {
		const newPolynomial = '4..\t';
		cy.get('input').first().type(`${newPolynomial}`);
		cy.get('input').first().blur();
		cy.get('input').first().parent().should('have.class', 'invalid');
	});

	it('forces interation count to 10,000 if a larger value is entered', () => {
		const iterationCount = '0000';
		cy.get('input').eq(2).type(`${iterationCount}`);
		cy.get('input').eq(2).blur();
		cy.get('input').eq(2).should('have.value', '10000');
	});
});
