/// <reference types="Cypress" />

describe('landing form with backend server', () => {
	beforeEach(() => {
		cy.visit('http://localhost:5173/form/');
		cy.viewport('macbook-11');
	});

	it('shows charts component if inputs are valid', () => {
		cy.get('input').first().type('1');
		cy.get('input').first().blur();
		cy.get('input').eq(1).type('n');
		cy.get('input').eq(1).blur();
		cy.wait(1000);
		cy.get('button').focus().click({ force: true }).trigger('click');
		cy.wait(3000);
		cy.get('div.chart-container').should('be.visible');
	});
});
