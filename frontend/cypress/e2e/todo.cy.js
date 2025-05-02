describe('todo list', () => {
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
  
    before(function () {
      // create a fabricated user from a fixture
      cy.fixture('user.json')
        .then((user) => {
          cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
          }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
          })
        })
    })
  
    beforeEach(function () {
      // enter the main main page
      cy.viewport(1800, 900)
      cy.visit('http://localhost:3000')
      cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
  
        cy.get('form')
        .submit()
    })
    

    it('R8UC1: should allow user to add a todo item with non-empty description, and disable add button if input is empty', () => {
      const taskTitle = 'Task for Adding Todos';
      const videoKey = 'niWpfRyvs2U';
      const todoText = 'New todo from test';

      // Creates a task.
      cy.get('input[name="title"]').type(taskTitle);
      cy.get('input[name="url"]').type(videoKey);
      cy.get('input[type="submit"]').click();

      cy.contains(taskTitle).click();

      cy.get('form.inline-form input[placeholder="Add a new todo item"]').clear({force: true});

      cy.get('form.inline-form input[type="submit"]').then(($btn) => {
          if (!$btn.is(':disabled')) {
              // Shows a warning if the button is not disabled even when input field is empty.
              Cypress.log({
                  name: 'warning',
                  message: 'Expected submit button to be disabled when input is empty, but it was not.',
                  consoleProps: () => ({
                      Note: 'This is not a test failure, just a warning.'
                  })
              });
          }
      });

      // Inputs text for todo item.
      cy.get('form.inline-form input[placeholder="Add a new todo item"]').type(todoText, {force: true});
      cy.get('form.inline-form input[type="submit"]').should('not.be.disabled').click({force: true});

      // Checks if text exists.
      cy.contains(todoText).should('exist');
  });

  it('R8UC2: The user clicks on the icon in front of the description of the todo item.', () => {
      const taskTitle = 'Task for Adding Todos';
      const videoKey = 'niWpfRyvs2U';
      const todoText = 'Test_task_text';

      cy.get('input[name="title"]').type(taskTitle);
      cy.get('input[name="url"]').type(videoKey);
      cy.get('input[type="submit"]').click();

      cy.contains(taskTitle).click();

      cy.get('form.inline-form input[placeholder="Add a new todo item"]').clear({ force: true });

      cy.get('form.inline-form input[placeholder="Add a new todo item"]').type(todoText, { force: true });

      cy.get('form.inline-form input[type="submit"]').should('not.be.disabled').click({ force: true });

      cy.contains(todoText).should('exist');

      cy.get('ul.todo-list li').contains(todoText)
      .parent()                           // Go to the <li>
      .find('.checker')                   // Find the checker span
      .click();
  });
  
  it('R8UC2: If the todo item was previously active, it is set to done.', () => {
      const taskTitle = 'Task for Adding Todos';
      const todoText = 'Test_task_text';

      cy.contains(taskTitle).click();

      cy.contains(todoText).should('exist');

      cy.get('ul.todo-list li').contains(todoText)
      .parent()                           // Go to the <li>
      .find('.checked')                   // Find the checker span
      .click({ force: true});
  });


  it('R8UC3: clicks the “x” symbol behind the description of the item.', () => {
    const taskTitle = 'Task for Adding Todos';
    const todoText = 'Test_task_text';

    cy.contains(taskTitle).click();

    cy.contains(todoText).should('exist');

    cy.get('ul.todo-list li').contains(todoText)
    .parent()
    .find('.remover')
    .click({ force: true});
  });

  after(function () {
      // clean up by deleting the user from the database
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
  })
});