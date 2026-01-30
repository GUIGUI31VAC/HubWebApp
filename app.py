from flask import Flask
from modules.dashboard.routes import dashboard_bp
from auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = "ton_secret_key"

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
