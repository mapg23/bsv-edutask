describe('todo list', () => {
    let uid;   // user id
    let name;
    let email;
    let taskId; // id of task

before(function () {
    cy.fixture('user.json').then(user => {
        cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
        }).then(response => {
        uid = response.body._id.$oid;
        email = user.email;

        // Visit site and create task
        cy.visit('http://localhost:3000');

        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email);

        cy.get('form').submit();

        cy.get('input[name=title]').type('Task for Adding Todos');

        cy.get('input[name=url]').type('niWpfRyvs2U');

        cy.get('input[type=submit][value="Create new Task"]').click();
        });
    });
});

beforeEach(function () {
    cy.viewport(1800, 900);
    cy.visit('http://localhost:3000');

    cy.contains('div', 'Email Address')
    .find('input[type=text]')
    .type(email);

    cy.get('form').submit();

    cy.contains('Task for Adding Todos').click();
});

it('R8UC1: should allow user to add a todo item with non-empty description, and disable add button if input is empty', () => {
    const todoText = 'New todo from test';

    cy.get('form.inline-form input[placeholder="Add a new todo item"]').clear({ force: true });
    cy.get('form.inline-form input[type="submit"]');

    cy.get('form.inline-form input[placeholder="Add a new todo item"]').type(todoText, { force: true });
    cy.get('form.inline-form input[type="submit"]').should('not.be.disabled').click({ force: true });

    cy.contains(todoText).should('exist');
});

it('R8UC2: The user clicks on the icon in front of the description of the todo item.', () => {
    const todoText = 'New todo from test';

    cy.get('form.inline-form input[placeholder="Add a new todo item"]').clear({ force: true });

    cy.get('form.inline-form input[placeholder="Add a new todo item"]').type(todoText, { force: true });

    cy.get('form.inline-form input[type="submit"]').should('not.be.disabled').click({ force: true });

    cy.contains(todoText).should('exist');

    cy.get('ul.todo-list li').contains(todoText)
    .parent()                           // Go to the <li>
    .find('.checker')                   // Find the checker span
    .click();
});

it('R8UC3: clicks the “x” symbol behind the description of the item.', () => {
    const todoText = 'New todo from test';

    cy.contains(todoText).should('exist');

    cy.get('ul.todo-list li').contains(todoText)
    .parent()
    .find('.remover')
    .click({ force: true});
});

after(function () {
    // Remove user through backend
    cy.request({
    method: 'DELETE',
    url: `http://localhost:5000/users/${uid}`
    }).then(response => {
    cy.log(response.body);
    });
});
});
