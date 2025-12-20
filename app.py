from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.profile_controller import profile_bp
from models.user_model import init_db

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Initialize DB
init_db()

# Register controllers
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)

if __name__ == "__main__":
    app.run(debug=True)