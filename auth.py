"""
auth.py — Kirjautuminen ja Flask-Login-integraatio VitalsDemo-sovellukselle.
"""

import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

import models

auth_bp = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"


class User(UserMixin):
    """Kevyt käyttäjäobjekti Flask-Loginia varten (ei säilytä salasanaa)."""

    def __init__(self, id, username, role):
        self.id = str(id)
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    row = models.get_user_by_id(user_id)
    if row is None:
        return None
    return User(row["id"], row["username"], row["role"])


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.patients_list"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        row = models.get_user_by_username(username)

        if row is not None and bcrypt.checkpw(
            password.encode("utf-8"), row["password_hash"].encode("utf-8")
        ):
            login_user(User(row["id"], row["username"], row["role"]))
            return redirect(url_for("main.patients_list"))

        error = "Väärä käyttäjätunnus tai salasana."

    return render_template("login.html", error=error)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
