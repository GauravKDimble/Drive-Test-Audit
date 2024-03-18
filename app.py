from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore, auth
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask import flash
from firebase_admin import auth

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase
cred = credentials.Certificate("C:\\Users\\Gaurav\\Downloads\\telecom-tower-performance-1-firebase-adminsdk-76b3k-265f93b36b.json")  # Update with your own service account key
firebase_admin.initialize_app(cred)
db = firestore.client()

# Password regex pattern
password_regex = re.compile(r'^(?=.*[A-Z])(?=.*\d{2})(?=.*[!@#$%^&*()-+=])[A-Za-z\d!@#$%^&*()-+=]{6,}$')

@app.route("/")
def home():
    return redirect(url_for('welcome'))

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        circle_name = request.form['circle_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Check if passwords match
        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            return render_template('signup.html', error=error_message)

        # Validate password format
        if not password_regex.match(password):
            error_message = "Password should contain at least six characters, one uppercase letter, two digits, and one special symbol."
            return render_template('signup.html', error=error_message)

        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,


            )

            # Store additional user data in Firestore
            user_ref = db.collection('users').document(user.uid)
            user_ref.set({
                'employee_Name': employee_name,
                'circle_name': circle_name,
                'email': email,
                'password': generate_password_hash(password),
                'isAdmin': False # Store hashed password
            })

            # Redirect to login page after successful registration
            success_message = "Registration successful! You can now login."
            return redirect(url_for('login', success=success_message))
        except auth.EmailAlreadyExistsError:
            error_message = "Email already exists. Please choose a different one."
            return render_template('signup.html', error=error_message)
        except Exception as e:
            print('Error creating user:', e)
            error_message = "Registration failed. Please try again."
            return render_template('signup.html', error=error_message)

    return render_template('signup.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.get_user_by_email(email)  # Get user from Firebase Authentication
            user_data = db.collection('users').document(user.uid).get().to_dict()

            if check_password_hash(user_data['password'], password):  # Verify password
                if user_data.get('isAdmin', True):  # Check if user is an admin
                    return render_template('projectselection.html')
                else:
                    return render_template('userreques.html')
            else:
                flash("Invalid email or password. Please try again.")



        except auth.UserNotFoundError:
            flash("User not found.")
        except Exception as e:
            print('Error logging in:', e)
            flash("An unexpected error occurred. Please try again.")

    return render_template('login.html')
@app.route("/taskallocation", methods=['GET', 'POST'])
def task_allocation():
    if request.method == 'POST':
        # Any processing you want to do when the form is submitted

        # Redirect to the task allocation page
        return redirect(url_for('task_allocation'))

    # Render the task allocation page template for GET requests
    return render_template('Taskallocation.html')

@app.route("/userrequests")
def user_requests():
    return render_template('userreques.html')







if __name__ == '__main__':
    app.run(debug=True)