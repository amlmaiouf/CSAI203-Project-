from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from app.database import get_db_connection, DB_CONFIG


login_manager = LoginManager()


def initialize_admin_user():
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()


        cursor.execute("SELECT COUNT(*) FROM [User] WHERE role = 'Admin'")
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:

            hashed_password = generate_password_hash('admin123')

            cursor.execute("""
                INSERT INTO [User] (name, email, password, role, phone_number, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                'Admin User',
                'admin@elderlycare.com',
                hashed_password,
                'Admin',
                '01011111111',
                'Cairo, Egypt'
            ))
            conn.commit()
            print("[OK] Default admin user created!")
            print("   Email: admin@elderlycare.com")
            print("   Password: admin123")
        else:
            print("[OK] Admin user already exists")

        return True
    except Exception as e:
        print(f"Error creating admin: {e}")
        return False
    finally:
        conn.close()


def initialize_sample_services():
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()


        cursor.execute("SELECT COUNT(*) FROM [Service]")
        service_count = cursor.fetchone()[0]

        if service_count == 0:
            services = [
                ('Home Doctor Visit', 'Medical', 500.00, 'A specialized doctor visits your home for examination and consultation.'),
                ('Nursing Service', 'Nursing', 300.00, 'Complete home nursing service with trained nurses.'),
                ('Home Cleaning', 'Housekeeping', 200.00, 'Comprehensive home cleaning service.'),
                ('Laundry Service', 'Housekeeping', 100.00, 'Laundry washing and ironing service.'),
                ('Medication Delivery', 'Pharmacy', 50.00, 'Delivery of medications from the pharmacy to your home.'),
                ('Grocery Delivery', 'Grocery', 75.00, 'Delivery of supermarket purchases.'),
                ('Pet Care', 'Pet Care', 150.00, 'Care and feeding of pets.'),
                ('Car Cleaning', 'Car Cleaning', 120.00, 'Car cleaning service at home.'),
                ('Companionship', 'Companionship', 250.00, 'Companionship and care service for the elderly.'),
            ]

            for service in services:
                cursor.execute("""
                    INSERT INTO [Service] (service_name, type, price, description, is_available)
                    VALUES (?, ?, ?, ?, 1)
                """, service)

            conn.commit()
            print(f"[OK] {len(services)} sample services created!")
        else:
            print(f"[OK] Services already exist ({service_count} found)")

        return True
    except Exception as e:
        print(f"Error creating services: {e}")
        return False
    finally:
        conn.close()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../templates', static_url_path='')


    app.config['SECRET_KEY'] = 'elderly_care_secret_key_2025'


    app.config['DB_CONFIG'] = DB_CONFIG


    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    from app.controllers.main_controller import main_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.housekeeping_controller import housekeeping_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(housekeeping_bp)


    with app.app_context():
        conn = get_db_connection()
        if conn:
            print("[OK] Connected to SQL Server database successfully!")
            conn.close()


            print("\n--- Initializing Data ---")
            initialize_admin_user()
            initialize_sample_services()
            print("-------------------------\n")
        else:
            print("[ERROR] Failed to connect to database. Check your DB_CONFIG settings.")

    return app
