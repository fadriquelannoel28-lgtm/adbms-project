from datetime import datetime 
import os

from flask import Flask, flash, flash, redirect, render_template, request, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import User, db
from functools import wraps
from flask_login import login_required, current_user, LoginManager, login_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin123@127.0.0.1:3306/medstock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'medsave_key'

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect('/login')

# ------------------------------------------------------------------------------------------------------------------
@app.route('/Dashboard/user-<int:user_id>/<name>')
@login_required
def dashboard(user_id, name): # Add these here
    return render_template('index.html', page_title='Dashboard', u_id=user_id, u_name=name)

# ------------------------------------------------------------------------------------------------------------------
@app.route('/Inventory-Management/user-<int:user_id>/<name>')
@login_required
def inventory_management(user_id, name):
    return render_template('minventory.html', page_title='Inventory Management', u_id=user_id, u_name=name)

# ------------------------------------------------------------------------------------------------------------------
@app.route('/Stock-Monitoring/user-<int:user_id>/<name>')
@login_required
def stock_monitoring(user_id, name):
    return render_template('smonitoring.html', page_title='Stock Monitoring', u_id=user_id, u_name=name)

# ------------------------------------------------------------------------------------------------------------------
@app.route('/Ordering-System/user-<int:user_id>/<name>')
@login_required
def ordering_system(user_id, name):
    return render_template('orderings.html', page_title='Ordering System', u_id=user_id, u_name=name)

# ------------------------------------------------------------------------------------------------------------------
@app.route('/Reports/user-<int:user_id>/<name>')
@login_required
def reports(user_id, name):
    return render_template('reports.html', page_title='Reports', u_id=user_id, u_name=name)

# ------------------------------------------------------------------------------------------------------------------
@app.route('/User-Access/user-<int:user_id>/<name>')
@login_required
def user_access(user_id, name):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', 
                           page_title='User Access', 
                           u_id=user_id, u_name=name, 
                           u_profile_pic=user.profile_pic, 
                           u_firstname=user.first_name, 
                           u_lastname=user.last_name,
                           u_middlename=user.middle_name,
                           u_gender=user.gender,
                           u_phone=user.phone,
                           u_email=user.email,
                           u_birthdate=user.birthdate)

# ------------------------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            first_name = request.form.get('firstname'),
            last_name = request.form.get('lastname'),
            email = request.form.get('email'),
            username = request.form.get('username'),
            password_hash = generate_password_hash(request.form.get('password'))
        )
        try:
            db.session.add(new_user)
            db.session.commit() 
            return redirect(url_for('login')) 
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}"
        
    return render_template('register.html')

# ------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u_name = request.form.get('username')
        u_pass = request.form.get('password')

        user = User.query.filter_by(username=u_name).first()

        if user and check_password_hash(user.password_hash, u_pass):
            login_user(user) 
            
            session['user_id'] = user.id
            session['username'] = user.username
            
            return redirect(url_for('dashboard', user_id=user.id, name=user.username))        
        return "Invalid Username or Password"

    return render_template('login.html')
# ------------------------------------------------------------------------------------------------------------------ buttons

@app.route('/upload-profile/<int:user_id>', methods=['POST'])
@login_required
def upload_profile(user_id):
    file = request.files.get('profile_img')
    
    if file and file.filename != '':
        filename = f"user_{user_id}_profile.png"
        file_path = os.path.join('static/images', filename)
        
        file.save(file_path)
        
        user = User.query.get(user_id)
        user.profile_pic = filename
        db.session.commit()
        
    return redirect(url_for('user_access', user_id=user_id, name=user.username))

@app.route('/edit_profile/<int:user_id>', methods=['POST'])
@login_required
def edit_profile(user_id):
    # If the user_id in the URL doesn't match the logged-in user, block it
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if current_user.id != user_id:
        return "Unauthorized Action", 403
    
    user = User.query.get_or_404(user_id)
    
    # Update text fields
    user.first_name = request.form.get('edit_firstname')
    user.middle_name = request.form.get('edit_middlename')
    user.last_name = request.form.get('edit_lastname')
    user.gender = request.form.get('edit_gender')
    user.phone = request.form.get('edit_phone')
    user.email = request.form.get('edit_email')

    # Update date properly (only once)
    date_str = request.form.get('edit_birthdate')
    if date_str:
        try:
            # Convert string from HTML form to a Python date object
            user.birthdate = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Date conversion failed")
            return "Invalid date format", 400

    try:
        db.session.commit()
        flash("Profile updated successfully!", "success")
        # Redirect back to the access page
        return redirect(url_for('user_access', user_id=user.id, name=user.first_name))
    except Exception as e:
        db.session.rollback()
        return f"Database Error: {e}", 500
        
# ------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        from models import User 
        db.create_all() 
    app.run(debug=True)