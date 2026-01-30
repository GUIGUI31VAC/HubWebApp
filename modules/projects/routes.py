from flask import Blueprint, render_template, request, redirect, url_for, session
from db.database import get_db

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")

# --- Liste des projets ---
@projects_bp.route("/")
def list_projects():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM projects WHERE user_id=%s", (session["user_id"],))
        projects = cursor.fetchall()
    connection.close()
    
    return render_template("projects/list.html", projects=projects)

# --- Créer un projet ---
@projects_bp.route("/create", methods=["GET", "POST"])
def create_project():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        project_type = request.form["project_type"]
        
        connection = get_db()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO projects (user_id, name, description, project_type) VALUES (%s, %s, %s, %s)",
                (session["user_id"], name, description, project_type)
            )
            connection.commit()
        connection.close()
        return redirect(url_for("projects.list_projects"))
    
    return render_template("projects/create.html")

# --- Modifier un projet ---
@projects_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_project(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM projects WHERE id=%s AND user_id=%s", (id, session["user_id"]))
        project = cursor.fetchone()
    
    if not project:
        return redirect(url_for("projects.list_projects"))
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        project_type = request.form["project_type"]
        status = request.form["status"]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE projects SET name=%s, description=%s, project_type=%s, status=%s WHERE id=%s AND user_id=%s",
                (name, description, project_type, status, id, session["user_id"])
            )
            connection.commit()
        connection.close()
        return redirect(url_for("projects.list_projects"))
    
    connection.close()
    return render_template("projects/edit.html", project=project)

# --- Supprimer un projet ---
@projects_bp.route("/delete/<int:id>")
def delete_project(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM projects WHERE id=%s AND user_id=%s", (id, session["user_id"]))
        connection.commit()
    connection.close()
    return redirect(url_for("projects.list_projects"))
