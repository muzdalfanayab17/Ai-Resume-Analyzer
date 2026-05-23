from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pdfplumber
import os

app = Flask(__name__)
app.secret_key = "secretkey"

# DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "uploads"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ---------------- MODELS ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)


with app.app_context():
    db.create_all()

# ---------------- ROLE CHECK ---------------- #

def is_admin():
    return 'user' in session and session.get('role') == 'admin'

# ---------------- REGISTER ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        if User.query.filter_by(username=request.form['username']).first():
            return "Username already exists"

        hashed_pw = bcrypt.generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        user = User(
            username=request.form['username'],
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template("register.html")

# ---------------- LOGIN ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # ADMIN LOGIN
        if request.form['username'] == "admin" and request.form['password'] == "admin123":
            session['user'] = "admin"
            session['role'] = "admin"
            return redirect('/dashboard')

        # USER LOGIN
        user = User.query.filter_by(username=request.form['username']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            session['user'] = user.username
            session['role'] = user.role
            return redirect('/dashboard')

        return "Invalid login"

    return render_template("login.html")

# ---------------- LOGOUT ---------------- #

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return render_template("dashboard.html")

# ---------------- CV PAGE ---------------- #

@app.route('/cv')
def cv():
    if 'user' not in session:
        return redirect('/login')

    return render_template("index.html")

# ---------------- CV ANALYSIS ---------------- #

skills = ["python", "flask", "sql", "html", "css"]

@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['cv']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    text = text.lower()

    found = []
    missing = []

    for s in skills:
        if s in text:
            found.append(s)
        else:
            missing.append(s)

    score = int((len(found) / len(skills)) * 100)

    return render_template(
        "result.html",
        score=score,
        found=found,
        missing=missing
    )

# ---------------- ADMIN PANEL ---------------- #

@app.route('/admin')
def admin():
    if not is_admin():
        return render_template("access.html")

    jobs = Job.query.all()
    return render_template("admin.html", jobs=jobs)

# ---------------- ADD JOB ---------------- #

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if not is_admin():
        return render_template("access.html")

    if request.method == 'POST':
        job = Job(
            title=request.form['title'],
            description=request.form['description']
        )
        db.session.add(job)
        db.session.commit()
        return redirect('/admin')

    return render_template("add_job.html")

# ---------------- DELETE JOB ---------------- #

@app.route('/delete/<int:id>')
def delete(id):
    if not is_admin():
        return render_template("access.html")

    job = Job.query.get(id)
    db.session.delete(job)
    db.session.commit()
    return redirect('/admin')

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
