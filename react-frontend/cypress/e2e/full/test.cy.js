/// <reference types="Cypress" />

describe('landing form with backend server', () => {
	beforeEach(() => {
		cy.visit('http://localhost:5173');
		cy.viewport('macbook-11');
	});

	it('shows charts component if inputs are valid', () => {
		cy.get('input').first().type('4x^2-1');
		cy.get('input').first().blur();
		cy.get('input').eq(1).type('3x^4-2x+5');
		cy.get('input').eq(1).blur();
		cy.wait(1000);
		cy.get('button').focus().click({ force: true }).trigger('click');
		cy.get('div.chart-container').should('be.visible');
	});
});
