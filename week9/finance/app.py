import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get list of user's stocks and shares
    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM history WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        session["user_id"],
    )

    # Update price and value of every stock
    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote is not None:
            stock["price"] = quote["price"]
            stock["value"] = stock["price"] * stock["shares"]

    # Get user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash[0]["cash"]

    # Calculate total
    total = cash + sum(stock["value"] for stock in stocks)

    # Render template
    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # User's input
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please enter a symbol.")
        quote = lookup(symbol)
        if not quote:
            return apology("Please enter a valid symbol.")
        shares = request.form.get("shares")
        if not shares or not shares.isdigit():
            return apology("Please enter a number of shares to buy.")
        shares = int(shares)
        if shares < 1:
            return apology("Please enter a valid number of shares.")
        cost = shares * quote["price"]

        # Get user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        # Shares validation check
        if cash < cost:
            return apology(f"You have insufficient cash to purchase {shares} shares.")

        # Update database
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", cash - cost, session["user_id"]
        )
        db.execute(
            "INSERT INTO history (user_id, transaction_type, symbol, price, shares) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            "Buy",
            quote["symbol"],
            quote["price"],
            shares,
        )

        # Flash message
        flash(f"You have successfully bought {shares} share(s) of {quote['symbol']}!")

        # Go back to index
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # User's input
        current_password = request.form.get("current_password")
        if not current_password:
            return apology("Please enter your current password.")
        new_password = request.form.get("new_password")
        if not new_password:
            return apology("Please enter your new password.")
        new_confirmation = request.form.get("new_confirmation")
        if not new_confirmation:
            return apology("Please enter your new password confirmation.")
        if new_password != new_confirmation:
            return apology("Please enter the same password and password confirmation.")

        # Update database
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new_password),
            session["user_id"],
        )

        # Flash
        flash("You have successfully changed your password!")

        return redirect("/")

    else:
        return render_template("change_password.html")


@app.route("/history")
@login_required
def history():
    history = db.execute(
        "SELECT * FROM history WHERE user_id = ? ORDER BY datetime DESC",
        session["user_id"],
    )
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # User's input
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please enter a symbol.")

        # Get quote
        quote = lookup(symbol)
        if not quote:
            return apology("Please enter a valid stock symbol.")

        # Load quoted page
        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # User's input
        username = request.form.get("username")
        if not username:
            return apology("Please enter a username.")
        existing_usernames = db.execute("SELECT username FROM users")
        for existing_username in existing_usernames:
            if existing_username["username"] == username:
                return apology(
                    "This username already exists. Please enter a new username."
                )
        password = request.form.get("password")
        if not password:
            return apology("Please enter a password.")
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Please enter a password confirmation.")
        if password != confirmation:
            return apology("Please enter the same password and password confirmation.")

        # Add user to database and log user in
        session["user_id"] = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password),
        )

        return redirect("/")

    # If GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get list of user's stocks and shares
    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM history WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        session["user_id"],
    )

    # Get list of user's symbols
    symbols = [stock["symbol"] for stock in stocks]

    if request.method == "POST":
        # User's input
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please enter a symbol.")
        quote = lookup(symbol)
        if not quote:
            return apology("Please enter a valid symbol.")
        shares = request.form.get("shares")
        if not shares or not shares.isdigit():
            return apology("Please enter a number of shares to sell.")
        shares = int(shares)
        if shares < 1:
            return apology("Please enter a valid number of shares.")
        profit = shares * quote["price"]

        # Get user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        # Validate symbol
        if quote["symbol"] not in symbols:
            return apology("Please enter the symbol of a stock you own.")

        # Validate shares
        for stock in stocks:
            if stock["symbol"] == symbol and stock["shares"] < shares:
                return apology(
                    f"You have {stock['shares']} shares of {stock['symbol']}. You do not have enough shares of this stock to sell {shares} shares. Please enter a valid number of shares."
                )

        # Update database
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", cash + profit, session["user_id"]
        )
        db.execute(
            "INSERT INTO history (user_id, transaction_type, symbol, price, shares) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            "Sell",
            quote["symbol"],
            quote["price"],
            -shares,
        )

        # Flash message
        flash(f"You have successfully sold {shares} share(s) of {quote['symbol']}!")

        return redirect("/")

    else:
        return render_template("sell.html", symbols=symbols, stocks=stocks)
