from flask import Blueprint, render_template, request, session, redirect
import database
from auth import login_required
from werkzeug.security import check_password_hash

web = Blueprint("web", __name__)

@web.route("/")
@login_required
def home():
    return render_template("index.html"), 200

# ----------------
# LOGIN ROUTE
# ----------------

@web.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = database.get_user_by_username(username)
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect("/")
        else:
            error = "Invalid credentials!"
    return render_template("login.html", error=error)   