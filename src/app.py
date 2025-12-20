from flask import Flask
from controllers.housekeeping_controller import housekeeping_bp

app = Flask(
    __name__,
    template_folder="../templates",  # templates folder
    static_folder="../templates"     # CSS, images, fonts folder
)

app.register_blueprint(housekeeping_bp)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)
