/// <reference types="Cypress" />

describe('landing form', () => {
	beforeEach(() => {
		cy.visit('http://localhost:5173');
		cy.viewport('macbook-11');
	});

	const invalidMathInput = `4..`;

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
		cy.get('input').first().type(invalidMathInput);
		cy.get('input').first().blur();
		cy.wait(1000);
		cy.get('input').first().parent().should('have.class', 'invalid');
	});

	it('should display an error message when an input is invalid', () => {
		cy.get('div.error-message').should('not.be.visible');
		cy.get('input').first().type(invalidMathInput);
		cy.get('input').first().blur();
		cy.wait(1000);
		cy.get('div.error-message').should('be.visible');
	});

	it('should display an error message when an input contains more than one variable', () => {
		cy.get('div.error-message').should('not.be.visible');
		cy.get('input').first().type('4x-3y+1');
		cy.get('input').first().blur();
		cy.wait(1000);
		cy.get('div.error-message').should('be.visible');
	});

	it('should display an error message when the inputs combined contain more than one variable', () => {
		cy.get('div.error-message').should('not.be.visible');
		cy.get('input').first().type('4x^2-1');
		cy.get('input').eq(1).type('3y^4-2y');
		cy.get('input').eq(1).blur();
		cy.wait(1000);
		cy.get('div.error-message').eq(2).should('be.visible');
	});

	it('strips characters not used in math expressions', () => {
		const newPolynomial = `4!@#$%&_={}[]|~\`<>\\?,+1	
		`;
		cy.get('input').first().type(`${newPolynomial}`);
		cy.get('input').first().blur();
		cy.wait(1000);
		cy.get('input').first().should('have.value', '4+1');
	});

	it('mangles script tags', () => {
		const newPolynomial = '<script>console.log("hello")</script>';
		cy.get('input').first().type(`${newPolynomial}`);
		cy.get('input').first().blur();
		cy.wait(1000);
		cy.get('input').first().should('not.contain', '<script>');
		cy.get('input').first().should('not.contain', '</script>');
	});

	it('sets the form as invalid if one of the polynomials is invalid', () => {
		cy.get('form').first().should('have.class', 'invalid');
	});

	it('forces interation count to 10,000 if a larger value is entered', () => {
		const iterationCount = '0000';
		cy.get('input').eq(2).type(`${iterationCount}`);
		cy.get('input').eq(2).blur();
		cy.wait(1000);
		cy.get('input').eq(2).should('have.value', '10000');
	});

	it('shows charts component if inputs are valid', () => {
		cy.get('input').first().type('4x^2-1');
		cy.get('input').first().blur();
		cy.get('input').eq(1).type('3x^4-2x+5');
		cy.get('input').eq(1).blur();
		cy.wait(1000);
		cy.get('button').focus().click({ force: true }).trigger('click');
		//cy.intercept('POST', 'http://localhost:8000/analyze').as('analyze');
		//cy.wait('@analyze').then((interception) => {
		cy.get('div.chart-container').should('be.visible');
		//});
	});
});
