from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.feedback_model import FeedbackModel

feedback_bp = Blueprint('feedback', __name__)
feedback_model = FeedbackModel()

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        service_name = request.form.get('serviceName')
        rating = request.form.get('rating')
        user_name = request.form.get('userName')
        comment = request.form.get('comment')

        # Simple validation
        if not (service_name and rating and user_name and comment):
            flash('Please fill all fields', 'danger')
            return redirect(url_for('feedback.feedback'))

        # Save feedback
        feedback_model.create_feedback(service_name, int(rating), user_name, comment)
        flash('Thank you! Your feedback has been submitted.', 'success')
        return redirect(url_for('feedback.feedback'))

    return render_template('feedback.html')
