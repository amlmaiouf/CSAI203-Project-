from flask import Flask, render_template
from Controllers.payment_controller import payment_bp
from Controllers.feedback_controller import feedback_bp

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

app.register_blueprint(payment_bp)

app.register_blueprint(feedback_bp)
@app.route("/")
def home():
    return render_template("car_washing.html")  


if __name__ == "__main__":
    app.run(debug=True)
