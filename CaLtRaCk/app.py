import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime

from helpers import apology, login_required, check_password

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///caltrack.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure user's name was submitted
        if not request.form.get("name"):
            return apology("must provide your name", 400)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted again to be confirmed
        elif not request.form.get("confirmation"):
            return apology("must provide password to confirm", 400)

        # Ensure password and confirmation passowrd are same
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("Password and confirmation password must be same", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").upper())

        # Ensure username does not already exists
        if len(rows) != 0:
            return apology("Username already exists", 400)

        # Validate password rules
        if check_password(request.form.get("newpass")) == False:
            return apology("Password requirements are not fulfilled", 400)

        # To insert new user in the database
        db.execute("INSERT INTO users(username, hash, name) VALUES(?, ?, ?)", request.form.get("username").upper(), generate_password_hash(request.form.get("password")), request.form.get("name").upper())
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").upper())
        print(rows)
        session["user_id"] = rows[0]["id"]
        session["username"] = request.form.get("username").upper()
        session["name"] = request.form.get("name").upper()
        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").upper())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["name"] = rows[0]["name"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def index():
    """To calculate BMR"""
    rows = db.execute("SELECT gender, age, weight, height, activity, goal, BMR, cal FROM user_profile WHERE user_id = ?", session["user_id"])
    cal_today = db.execute("SELECT SUM(calories) AS sum FROM cal_logs WHERE user_id = ? and date = ?", session["user_id"], date.today())
    print(cal_today)
    if len(rows) == 0:
        return apology("Please set your profile", 400)
    else:
        if cal_today[0]["sum"] is None:
            rem_cal = rows[0]["cal"]
        else:
            rem_cal = rows[0]["cal"] - cal_today[0]["sum"]
        return render_template("index.html", rows=rows, cal_today=cal_today, rem_cal=rem_cal)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Show our profile"""
    if request.method == "GET":
        return render_template("profile.html")
    else:
        if not request.form.get("gender"):
            return apology("must provide gender", 400)

        # Ensure age was correctly submitted
        elif not request.form.get("age"):
            return apology("must provide age in positive numbers", 400)

        # Ensure weight was submitted
        elif not request.form.get("weight"):
            return apology("must provide weight in kilograms", 400)

        # Ensure height was submitted
        elif not request.form.get("height"):
            return apology("must provide height in centimeters", 400)

        # Ensure activity level was submitted
        elif not request.form.get("activity"):
            return apology("must provide activity level", 400)

        # Ensure health goal was submitted
        elif not request.form.get("goal"):
            return apology("must provide health goal", 400)

        if request.form.get("gender").upper() == 'M':
            bmr = 88.362 + (13.397 * float(request.form.get("weight"))) + (4.799 * float(request.form.get("height"))) - (5.677 * float(request.form.get("age")))
        else:
            bmr = 447.593 + (9.247 * float(request.form.get("weight"))) + (3.098 * float(request.form.get("height"))) - (4.330 * float(request.form.get("age")))

        if request.form.get("activity") == "sedantry":
            bmr = bmr * 1.2
        elif request.form.get("activity") == "active":
            bmr = bmr * 1.3
        elif request.form.get("activity") == "intense":
            bmr = bmr * 1.5

        if request.form.get("goal") == "maintain":
            cal = bmr
        if request.form.get("goal") == "gain":
            cal = bmr + 300
        if request.form.get("goal") == "loss":
            cal = bmr - 300
        bmr = round(bmr)
        cal = round(cal)

        rows = db.execute("SELECT user_id FROM user_profile WHERE user_id = ?", session["user_id"])
        if len(rows) == 0:
            db.execute("INSERT INTO user_profile VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("gender").upper(), request.form.get("age"), float(request.form.get("weight")), float(request.form.get("height")), request.form.get("activity"), request.form.get("goal"), bmr, cal)
        else:
            db.execute("UPDATE user_profile SET gender = ?, activity = ?, age = ?, weight = ?, height = ?, goal = ?, BMR = ?, cal = ? WHERE user_id = ?", request.form.get("gender").upper(), request.form.get("activity"), request.form.get("age"), float(request.form.get("weight")), float(request.form.get("height")), request.form.get("goal"), bmr, cal, session["user_id"])
        return redirect("/")


@app.route("/workout", methods=["GET", "POST"])
@login_required
def workout():
    """Show our workout notes"""
    logs = db.execute("SELECT log_id, logs, logged_time FROM workout_logs WHERE user_id = ? ORDER BY logged_time DESC", session["user_id"])
    if request.method == "GET":
        return render_template("workout.html", logs=logs)
    else:
        if not request.form.get("workout") and not request.form.get("delete"):
            return apology("must provide something to log", 400)

        elif request.form.get("delete") and request.method == "POST":
            db.execute("DELETE FROM workout_logs WHERE user_id = ? AND log_id = ?", session["user_id"], request.form.get("delete"))
            return redirect("/workout")

        else:
            log_id = db.execute("SELECT MAX(log_id) as log_id FROM workout_logs WHERE user_id = ?", session["user_id"])
            if log_id[0]["log_id"] is None:
                n_log_id = 1
            else:
                n_log_id = log_id[0]["log_id"] + 1
            db.execute("INSERT INTO workout_logs (user_id, log_id, logs) VALUES (?, ?, ?)", session["user_id"], n_log_id, request.form.get("workout"))
            return redirect("/workout")


@app.route("/cal_logs", methods=["GET", "POST"])
def cal_logs():
    """Logs calories"""
    logs = db.execute("SELECT date, SUM(calories) AS sum FROM cal_logs WHERE user_id = ? GROUP BY date ORDER BY date DESC, logged_time", session["user_id"])
    date_p = db.execute("SELECT DISTINCT date FROM cal_logs WHERE user_id = ? ORDER BY date DESC", session["user_id"])
    rows = db.execute("SELECT log_id, food, calories, date, logged_time FROM cal_logs WHERE user_id = ? AND date = ? ORDER BY logged_time asc", session["user_id"], date.today())
    if request.method == "GET":
        return render_template("cal_logs.html", logs=logs, date_p=date_p, rows=rows)

    elif request.form.get("view_logs") and request.method == "POST":
        if not request.form.get("view"):
            return apology("Please select a date to view logs", 400)
        rows = db.execute("SELECT log_id, food, calories, date, logged_time FROM cal_logs WHERE user_id = ? AND date = ? ORDER BY logged_time asc", session["user_id"], request.form.get("view"))
        return render_template("cal_logs.html", logs=logs, date_p=date_p, rows=rows)

    elif request.form.get("delete") and request.method == "POST":
        db.execute("DELETE FROM cal_logs WHERE user_id = ? AND log_id = ?", session["user_id"], request.form.get("delete"))
        return redirect("/cal_logs")

    else:
        if not request.form.get("food"):
            return apology("Please enter food to log", 400)
        elif not request.form.get("calories"):
            return apology("Please enter calories of food to log", 400)
        log_id = db.execute("SELECT MAX(log_id) as log_id FROM cal_logs WHERE user_id = ?", session["user_id"])

        if log_id[0]["log_id"] is None:
            n_log_id = 1

        else:
            n_log_id = log_id[0]["log_id"] + 1
        db.execute("INSERT INTO cal_logs (user_id, log_id, date, food, calories, logged_time) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], n_log_id, date.today(), request.form.get("food"), request.form.get("calories"), datetime.now().strftime("%H:%M:%S"))

        return redirect("/cal_logs")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change password"""
    if request.method == "GET":
        return render_template("changepassword.html")

    else:
        # Ensure old password was submitted
        if not request.form.get("oldpass"):
            return apology("must provide old password", 403)

        # Ensure password was submitted
        elif not request.form.get("newpass"):
            return apology("must provide new password", 403)

        # Ensure password was submitted again to be confirmed
        elif not request.form.get("confirmpass"):
            return apology("must provide confirmation password to confirm", 403)

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("oldpass")):
            return apology("invalid old password", 403)
        # Ensure password and confirmation passowrd are same
        else:
            if request.form.get("newpass") == request.form.get("confirmpass"):
                if check_password(request.form.get("newpass")) == False:
                    return apology("Password requirements are not fulfilled", 400)
                db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("newpass")), session["user_id"])
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")