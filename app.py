from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin, LoginManager, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from werkzeug.utils import secure_filename


# ---------------------
# APP CONFIG
# ---------------------

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change_this_secret')

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# 
# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------
# MODELS
# ---------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile_pic = db.Column(db.String(200), default='default.png')



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# ---------------------
# CREATE TABLES
# ---------------------
with app.app_context():
    db.create_all()


# ---------------------
# Image Save Helper
# ---------------------
def save_profile_image(file):
    if not file:
        return None

    allowed = ['jpg', 'jpeg', 'png']
    ext = file.filename.rsplit('.', 1)[-1].lower()

    if ext not in allowed:
        return None

    # secure filename
    filename = secure_filename(file.filename)

    # unique filename
    unique_name = f"user_{current_user.id}.{ext}"

    filepath = os.path.join("static/profile_pics", unique_name)
    file.save(filepath)

    return unique_name


# ---------------------
# AUTH ROUTES
# ---------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password']

        if not username or not password:
            flash("Username and password required.")
            return redirect('/register')

        exists = User.query.filter_by(username=username).first()
        if exists:
            flash("User already exists! Choose another username or login.")
            return redirect('/register')

        hashed_pass = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created. Please login.")
        return redirect('/login')

    return render_template('register.html', title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
            return redirect('/login')

    return render_template('login.html', title="Login")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')


# ---------------------
# HOME / DASHBOARD
# ---------------------
@app.route('/')
@login_required
def home():
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    total_notes = Note.query.filter_by(user_id=current_user.id).count()
    return render_template('index.html', title="Dashboard",
                           total_tasks=total_tasks, total_notes=total_notes)


# ---------------------
# TASKS CRUD (AJAX add + pages)
# ---------------------
@app.route('/add-task', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()

    if not title:
        return jsonify({"status":"error","message":"Title required."}), 400

    new_task = Task(title=title, description=description, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"status": "success", "message": "Task saved!"})


@app.route('/tasks')
@login_required
def tasks():
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=all_tasks, title="My Tasks")


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash("Unauthorized.")
        return redirect('/tasks')

    if request.method == "POST":
        task.title = request.form['title'].strip()
        task.description = request.form['description'].strip()
        db.session.commit()
        flash("Task updated.")
        return redirect('/tasks')

    return render_template('edit.html', task=task, title="Edit Task")


@app.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash("Unauthorized.")
        return redirect('/tasks')
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.")
    return redirect('/tasks')


# ---------------------
# NOTES CRUD
# ---------------------
@app.route('/notes')
@login_required
def all_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes, title="Notes")


@app.route('/notes/add', methods=['GET', 'POST'])
@login_required
def add_note():
    if request.method == "POST":
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if not title:
            flash("Title required.")
            return redirect('/notes/add')
        new_note = Note(title=title, content=content, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note saved.")
        return redirect('/notes')

    return render_template('add_note.html', title="Add Note")


@app.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash("Unauthorized.")
        return redirect('/notes')

    if request.method == "POST":
        note.title = request.form['title'].strip()
        note.content = request.form['content'].strip()
        db.session.commit()
        flash("Note updated.")
        return redirect('/notes')

    return render_template('edit_note.html', note=note, title="Edit Note")


@app.route('/notes/delete/<int:id>')
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash("Unauthorized.")
        return redirect('/notes')
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.")
    return redirect('/notes')


# ---------------------------------
# SEARCH ROUTE
# ---------------------------------
@app.route('/search')
@login_required
def search():

    query = request.args.get('q', '').strip()

    if not query:
        return render_template('search.html', query="", results_tasks=[], results_notes=[])

    # Task search
    results_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        (Task.title.ilike(f"%{query}%") | Task.description.ilike(f"%{query}%"))
    ).all()

    # Note search
    results_notes = Note.query.filter(
        Note.user_id == current_user.id,
        (Note.title.ilike(f"%{query}%") | Note.content.ilike(f"%{query}%"))
    ).all()

    return render_template(
        'search.html',
        query=query,
        results_tasks=results_tasks,
        results_notes=results_notes
    )


# ---------------------
# PROFILE PAGE
# ---------------------

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title="Your Profile")


@app.route('/profile/update-username', methods=['POST'])
@login_required
def update_username():
    new_username = request.form['new_username'].strip()

    if not new_username:
        flash("Username cannot be empty!")
        return redirect('/profile')

    # Check duplicate
    exist = User.query.filter_by(username=new_username).first()
    if exist:
        flash("Username already taken")
        return redirect('/profile')

    current_user.username = new_username
    db.session.commit()
    flash("Username updated successfully.")
    return redirect('/profile')


@app.route('/profile/update-password', methods=['POST'])
@login_required
def update_password():
    old = request.form['old_password']
    new = request.form['new_password']

    # Check if old matches
    if not check_password_hash(current_user.password, old):
        flash("Old password is incorrect.")
        return redirect('/profile')

    if len(new) < 4:
        flash("Password must be at least 4 characters.")
        return redirect('/profile')

    current_user.password = generate_password_hash(new)
    db.session.commit()

    flash("Password changed successfully.")
    return redirect('/profile')

@app.route('/profile/update-photo', methods=['POST'])
@login_required
def update_photo():
    if 'profile_pic' not in request.files:
        flash("No file selected.")
        return redirect('/profile')

    file = request.files['profile_pic']

    if file.filename == '':
        flash("No file selected.")
        return redirect('/profile')

    image_name = save_profile_image(file)

    if not image_name:
        flash("Only JPG and PNG images allowed.")
        return redirect('/profile')

    # delete old photo except default
    if current_user.profile_pic != 'default.png':
        try:
            os.remove(os.path.join("static/profile_pics", current_user.profile_pic))
        except:
            pass

    current_user.profile_pic = image_name
    db.session.commit()

    flash("Profile picture updated.")
    return redirect('/profile')


# ---------------------
# Run
# ---------------------
if __name__ == "__main__":
    # debug=True for development
    app.run(debug=True)
    # app.run(debug=False)