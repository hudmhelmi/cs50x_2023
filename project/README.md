# 🐧 Planguin - A (Very Mildly) Penguin-Themed Task Manager!

#### Video Demo: https://youtu.be/bxJTUsxGve0

## Project Description

Welcome to Planguin, a task management web application! Planguin is built using the Flask framework, making it a great tool for organising your daily to-do lists!

**Features:**

- **User Accounts:** Create your Planguin account today and don't worry: we value your security, so we use secure password hashing to keep your secrets safe.

- **Chill and Manage Tasks:** Planguin lets you add, update, and delete tasks with ease. Swim through your to-do list in style!

- **Waddle Towards Productivity:** Mark tasks as completed and feel like a productive penguin, achieving your goals one task at a time.

- **Seek and Search:** Planguin helps you search for your tasks like an expert explorer. Never lose track of your fish-catching missions again!

## Files for Curious Penguins

1. `app.py`: This is the main Python file containing the Flask application and all the route handlers. It sets up the web server, connects to the database, and defines various routes for user registration, login, task management, and search. It also handles user authentication using password hashing and session management.

2. `planguin.db`: This is the SQLite database file that stores user information and task data. It contains two tables, "users" for storing user details and "tasks" for storing task information.

3. `planguin.db.sql`: These are the SQLite commands used to generate `planguin.db`.

4. `templates`: This directory contains HTML templates used for rendering the web pages. It includes the following templates:
   - `index.html`: The main page that displays your tasks, both pending and completed.
   - `login.html`: The login page where you can enter your credentials to access your account.
   - `register.html`: The registration page where you can create a new account.
   - `change.html`: The page used for changing your username or password.
   - `layout.html`: The layout containing elements such as a navbar and flashes, from which all pages are extended.

5. `static`: This directory contains custom styles.
   - `styles.css`: This contains a variety of styles to customize the look of all the pages, building on the default styles provided by Bootstrap.

## Design Choices

1. **Flask**: We chose Flask as it's a lightweight and easy-to-use web framework, perfect for this project. It provides the necessary tools for routing, handling HTTP requests, and rendering templates.

2. **Bootstrap**: We embraced Bootstrap, enabling quick theming of all the pages and ensuring a consistent and visually appealing experience.

3. **SQLite3**: For its simplicity and self-contained nature, we opted for SQLite3 as the database system. As this application doesn't require complex data relationships, SQLite is a suitable choice.

4. **Password Hashing**: Your security matters to us! We utilize the `generate_password_hash` and `check_password_hash` functions from `werkzeug.security` to securely hash and verify user passwords, ensuring your passwords are never stored in plain text.

5. **Consistent Error Handling**: Planguin includes error handling for various scenarios, such as empty form fields, duplicate usernames during registration, incorrect passwords during login, and non-existent tasks during updates and deletions. A smooth user experience is our priority.

6. **Separation of Concerns**: The code is organized into separate route handlers, enhancing readability and maintainability. Each route handles a specific functionality of the application, ensuring clarity.

7. **User Interface**: We designed simple HTML templates for the user interface, making it easy to understand and modify. A clean and intuitive design is key to a delightful experience.

8. **Dropdown Edit Menus**: To enhance your user experience, we integrated edit forms directly into the task table, making task management even more effortless!

## Please Note:
This task manager was designed as a final project for CS50x 2023. Bugs may be present. Do not deploy without looking through the source code and ensuring that program is robust.

Planguin embraces the chilly spirit of penguins to bring you a user-friendly and delightful task management experience. Let the penguin adventure begin! 🐧❄️
