from core import create_app

# 1. IMPORT THE CONTROLLER
# We must import this so Python executes the file and loads the routes (Home, Login, etc.)
# However, we do NOT need to register it manually, because create_app is doing it for us.
from controllers.main_controller import main_controller

# Create the application instance
app = create_app('development')

# REMOVED: app.register_blueprint(main_controller) 
# (The line above caused the error because create_app already did this)

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, port=5000)