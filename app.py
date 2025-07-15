from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from livereload import Server

# App Config
app = Flask(__name__, template_folder='cybersecurity dashboard/templates')
app.secret_key = 'cyberlife'

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next') or url_for('dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(next_page)
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User.query.filter_by(username=username).first()

        # Check if username already exists
        if user:
            flash('Username already exists!', 'warning')
            return redirect(url_for('register'))

        # Create new user and add to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Forgot Password
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            return f"<h3>Password for {username}: <code>{user.password}</code></h3><a href='/login'>Login</a>"
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('forgot_password'))
    return render_template('forgot-password.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Feature Pages (All protected)
@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/challenge')
@login_required
def challenge():
    return render_template('cyber_arena_challenges.html')


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    # Watch for changes in the templates folder
    server.watch('cybersecurity dashboard/templates/*.html')  
    app.run(debug=True, port=5000)
