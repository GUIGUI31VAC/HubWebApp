from flask import Flask
from modules.dashboard.routes import dashboard_bp
from modules.projects.routes import projects_bp
from auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = "ton_secret_key"

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(projects_bp)

if __name__ == "__main__":
    app.run()
