from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from db.database import get_db
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        connection = get_db()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
        connection.close()
        
        if user:
            # Vérifie le mot de passe hashé (pour l'instant tu peux tester en clair)
            # if check_password_hash(user['password_hash'], password):
            if password == user.get('password_hash'):  # pour test, si tu n’as pas encore hash
                session["user"] = user["username"]
                session["user_id"] = user["id"]
                return redirect(url_for("dashboard.dashboard_home"))
            else:
                flash("Mot de passe incorrect", "error")
        else:
            flash("Utilisateur inconnu", "error")
    
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))