from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

# Setup flask
app = Flask(__name__)

# Connect database
db = SQL("sqlite:///planguin.db")

# Store session in filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Disable caching
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Route for the index page
@app.route("/")
def index():
    # Return to login pagee if no user is logged in
    if not session:
        return redirect("/login")

    # Retrieve the search input from the URL parameters
    search_input = request.args.get("search_input")
    if not search_input:
        search_input = "%"

    # Retrieve user information and tasks from the database
    username = db.execute(
        "SELECT username FROM users WHERE id = ?", session["user_id"]
    )[0]["username"]
    pending_tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND completed = 0 AND task_name LIKE ?",
        session["user_id"],
        search_input,
    )
    completed_tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND completed = 1",
        session["user_id"],
    )
    # Render the index.html template with user information and task data
    return render_template(
        "index.html",
        username=username,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
    )


# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username, password, password_confirmation = (
            request.form.get("username"),
            request.form.get("password"),
            request.form.get("password_confirmation"),
        )

        # Check if any field is blank
        if not username or not password or not password_confirmation:
            flash("Please fill in all fields.", "error")
            return redirect("/register")

        # Check if username already exists
        username_count = len(
            db.execute("SELECT username FROM users WHERE username = ?", username)
        )
        if username_count > 0:
            flash("Username taken. Please enter another username.", "error")
            return redirect("/register")

        # Check if password = password confirmation
        if password != password_confirmation:
            flash("Please enter the same password and password confirmation.", "error")
            return redirect("/register")

        # Insert user into database
        session["user_id"] = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password),
        )

        # Log user in
        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username = ?", username
        )[0]["id"]

        # Redirect user to index
        flash("You have registered successfully!", "success")
        return redirect("/")

    # If GET
    else:
        return render_template("register.html")


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")

        # Check if any field is blank
        if not username or not password:
            flash("Please fill in all fields.", "error")
            return redirect("/login")

        # Find user in database
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        # No user with username
        if len(user) == 0:
            flash("This user does not exist. Please enter a vaid username.", "error")
            return redirect("/login")
        # More than one user with username
        elif len(user) > 1:
            flash(
                "Admin error: there is more than one user with the same username, please contact support.",
                "error",
            )
            return redirect("/login")
        else:
            # Check if password is correct
            correct_hash = user[0]["hash"]
            if not check_password_hash(correct_hash, password):
                flash("Password is incorrect. Please enter a valid password.", "error")
                return redirect("/login")

        # Select user's id from database and log user in
        session["user_id"] = user[0]["id"]
        flash("You have logged in successfully!", "success")
        return redirect("/")

    # If GET
    else:
        return render_template("login.html")


# Route for user logout
@app.route("/logout")
def logout():
    # Clear the current session and redirect to the login page
    session.clear()
    return redirect("/login")


# Route: Add a new task to the database
@app.route("/add", methods=["POST"])
def add():
    # Retrieve the task information from the request form
    task_name, due_date = (
        request.form.get("task_name"),
        request.form.get("due_date"),
    )

    if not task_name or not due_date:
        flash("Please fill in all fields.", "error")
        return redirect("/")

    # Insert the new task into the database
    db.execute(
        "INSERT INTO tasks (user_id, task_name, due_date) VALUES (:user_id, :task_name, :due_date)",
        user_id=session["user_id"],
        task_name=task_name,
        due_date=due_date,
    )

    flash("Task added successfully", "success")
    return redirect("/")


# Route: Update an existing task in the database
@app.route("/update/<int:task_id>", methods=["POST"])
def update(task_id: int):
    # Retrieve the task information from the request form
    task_name, due_date = (
        request.form.get("task_name"),
        request.form.get("due_date"),
    )

    if not task_name or not due_date:
        flash("Please fill in all fields.", "error")
        return redirect("/")

    # Update the task in the database
    db.execute(
        "UPDATE tasks SET user_id=:user_id, task_name=:task_name, due_date=:due_date WHERE id = :task_id",
        user_id=session["user_id"],
        task_name=task_name,
        due_date=due_date,
        task_id=task_id,
    )
    flash("Task updated successfully", "success")
    return redirect("/")


# Route: Delete a task from the database
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id: int):
    # Get the task details from the database based on the task_id
    task = db.execute("SELECT * FROM tasks WHERE id = :task_id", task_id=task_id)
    if not task:
        flash("Task does not exist.", "error")
        return redirect("/")

    # Delete the task from the database
    db.execute("DELETE FROM tasks WHERE id = :task_id", task_id=task_id)
    flash("Task deleted successfully", "success")
    return redirect("/")


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id: int):
    # Get the task details from the database based on the task_id
    task = db.execute("SELECT * FROM tasks WHERE id = :task_id", task_id=task_id)
    if not task:
        flash("Task does not exist.", "error")
        return redirect("/")

    # Mark the task as completed in the database
    db.execute("UPDATE tasks SET completed = 1 WHERE id = :task_id", task_id=task_id)
    flash("Task completed successfully", "success")
    return redirect("/")


# Search
@app.route("/search", methods=["POST"])
def search():
    search_input = request.form.get("search_input")

    # If no input, reset task table to show all results
    if not search_input:
        return redirect("/")

    # Return input via URL parameter to index
    return redirect(f"/?search_input={search_input}")


# Change username
@app.route("/change_user", methods=["GET", "POST"])
def change_user():
    if request.method == "POST":
        username, password, password_confirmation = (
            request.form.get("username"),
            request.form.get("password"),
            request.form.get("password_confirmation"),
        )

        if not username or not password or not password_confirmation:
            flash("Please fill in all fields.", "error")
            return redirect("/change_user")

        # Check if passwords are the same
        if password != password_confirmation:
            flash("Please enter the same password and confirmation.", "error")
            return redirect("/change_user")

        # Check if password is valid
        hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0][
            "hash"
        ]
        if not check_password_hash(hash, password):
            flash("Please enter the correct password.", "error")
            return redirect("/change_user")

        # Check if username is taken
        if (
            len(db.execute("SELECT username FROM users WHERE username = ?", username))
            != 0
        ):
            flash("Username is already taken.", "error")
            return redirect("/change_user")

        # Update username in database
        db.execute(
            "UPDATE users SET username = ? WHERE id = ?", username, session["user_id"]
        )
        flash("Username updated successfully", "success")
        return redirect("/")

    else:  # GET
        return render_template("change.html")


# Change password
@app.route("/change_pass", methods=["GET", "POST"])
def change_pass():
    if request.method == "POST":
        new_pass, password, password_confirmation = (
            request.form.get("new_pass"),
            request.form.get("password"),
            request.form.get("password_confirmation"),
        )

        if not new_pass or not password or not password_confirmation:
            flash("Please fill in all fields.", "error")
            return redirect("/change_pass")

        # Check if passwords are the same
        if password != password_confirmation:
            flash("Please enter the same password and confirmation.", "error")
            return redirect("/change_pass")

        # Check if password is valid
        hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])[0][
            "hash"
        ]
        if not check_password_hash(hash, password):
            flash("Please enter the correct password.", "error")
            return redirect("/change_pass")

        # Update username in database
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new_pass),
            session["user_id"],
        )
        flash("Password updated successfully", "success")
        return redirect("/")

    else:  # GET
        return render_template("change.html")


if __name__ == "__main__":
    app.run(debug=True)
