from flask import Flask, render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "YouRuinedChickensColt"

connect_db(app)

@app.route("/")
def home():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_form():
    '''GET = makes the form'''
    """POST = processes the form"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        hashpass = User.register(username, pwd)
        """hashes the password and username"""
        user = User(username=hashpass.username, 
        password=hashpass.password, 
        email=email, 
        first_name=first_name,
        last_name=last_name)
        db.session.add(user)
        db.session.commit()

        session["user"] = user.username
        return redirect(f"/users/{user.username}")
    else:
        return render_template('add_user_form.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, pwd)

        if user:
            session["user"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login_form.html", form=form)
# end-login
    

@app.route("/users/<username>")
def secret(username):
    """Example hidden page for logged-in users only."""

    if "user" not in session: #validates user is logged in or returns home
        return redirect("/")
    else:
        user = User.query.get_or_404(username)
        return render_template('secret.html', user = user)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("user")
    return redirect("/")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "user" not in session: #validates user is logged in or returns home
        return redirect("/")
    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()

        return redirect('/login')

@app.route("/users/<username>/feedback/add", methods=["POST", "GET"])
def add_feedback(username):
    '''GET = makes the form'''
    """POST = processes the form"""
    form = FeedbackForm()
    if "user" not in session:
        return redirect('/login')
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title = title,
            content = content,
            username = username
        )
        
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template('feedback_form.html', form=form)
        
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Get: Shows feedback form"""
    """POST: Process feedback form"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect('/')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """if verified delete the feedback from the user"""

    feedback = Feedback.query.get(feedback_id)
    if "user" not in session or feedback.username != session['user']:
        return redirect('/')
    else:
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
