/// <reference types="cypress" />

context("Course Scheduler Page", () => {
  beforeEach(() => {
    cy.visit("/?semester=SUMMER 2020");
  });

  it("should show number of selected courses", () => {
    cy.get("[data-cy=num-selected-courses]").should("contain.text", "0");

    cy.get("[data-cy=course-search-tab] [data-cy=course-listing]")
      .eq(4)
      .find("[data-cy=name]")
      .should("have.text", "ARCH-4770")
      .click();

    cy.get("[data-cy=num-selected-courses]").should("contain.text", "1");
  });

  it("should show selected course listing", () => {
    cy.get("[data-cy=selected-courses-tab] [data-cy=course-listing]").should(
      "not.exist"
    );

    cy.get("[data-cy=course-search-tab] [data-cy=course-listing]")
      .eq(4)
      .find("[data-cy=name]")
      .should("have.text", "ARCH-4770")
      .click();

    cy.get("[data-cy=selected-courses-tab-header]").click();

    cy.get("[data-cy=selected-courses-tab] [data-cy=course-listing]").should(
      "have.length",
      1
    );
  });

  it("should add first section to schedule", () => {
    cy.get("[data-cy=schedule] [data-cy=schedule-event]").should("not.exist");
    cy.get("[data-cy=course-search-tab] [data-cy=course-listing]")
      .eq(4)
      .scrollIntoView()
      .find("[data-cy=name]")
      .should("have.text", "ARCH-4770")
      .click();
    cy.get("[data-cy=schedule] [data-cy=schedule-event]")
      .should("have.length", 6)
      .find("[data-cy=name]")
      .each(($el) => {
        cy.wrap($el).should("have.text", "ARCH 4770");
      });
  });

  it("should show course info modal", () => {
    cy.get("[data-cy=course-info-modal]").should("not.exist");
    cy.get("[data-cy=course-search-tab] [data-cy=course-listing]")
      .eq(4)
      .scrollIntoView()
      .find("[data-cy=course-info-button]")
      .click();
    cy.get("[data-cy=course-info-modal]").should("contain.text", "ARCH-4770");
  });
});
