from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, send, emit

from flask import render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin

from flask_login import login_user, current_user, logout_user, login_required
from pymongo import MongoClient

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


app = Flask(__name__)
app.secret_key = "thisKeyIsSuperSecure"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

client = MongoClient('localhost', 27017)
db = client.flask_db
users = db.users

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Assuming you have a User class in your models.py or wherever you define your data models

class User(UserMixin):
    def __init__(self, user_id, password, following=None, followers=None, about=None):
        self.id = user_id
        self.password = password
        self.about = about or ""
        self.following = following or []  # List to store usernames of users being followed
        self.followers = followers or []  # List to store usernames of users who follow this user

    def __repr__(self):
        return f"User('{self.id}', '{self.password}')"

    def is_following(self, other_user):
        return other_user['username'] in self.following
        #return other_user.username in self.following


@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({'username': user_id})
    if user_data:
        return User(
            user_id=user_data['username'],
            password=user_data['password'],
            followers=user_data.get('followers', []),
            following=user_data.get('following', []),
            about=user_data.get('about')
        )    
    return None


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user_data = users.find_one({'username': username.data})
        if user_data:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



@app.route("/")
def get_messages():
    return render_template('stream.html')

@app.route("/home")
def home():
    return render_template('home.html')

@socketio.on('connect')
def on_connect(data):
    send("This message will self-destruct in 10 seconds")


@socketio.on('message')
def on_message(data):
    user = data.get('user', 'Anonymous')
    message = f"{data['data']} --{user}"
    print(f"Message received: {message}")
    emit('message', message, broadcast=True)




@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username=form.username.data

        users.insert_one({'username': username, 'password': hashed_password})

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users.find_one({'username': form.username.data})
        user = load_user(user['username'])
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account', username=current_user.id)

@app.route("/profile/<username>")
@login_required
def public_profile(username):
    user_data = db.users.find_one({'username': username})
    if user_data:
        user = {
            'username': user_data['username'],
            'about': user_data.get('about', ''),
            'followers_count': len(user_data.get('followers', [])),
            'following_count': len(user_data.get('following', [])),
        }
        return render_template('profile.html', user=user)
    else:
        flash("User not found.", 'danger')
        return redirect(url_for('home'))
    
@app.route("/search", methods=['GET'])
def search_users():
    query = request.args.get('query', '').strip()

    if query:
        # Perform a case-insensitive search for users
        users = db.users.find({'username': {'$regex': f'{query}', '$options': 'i'}})
    else:
        # If no query is provided, display all users
        users = db.users.find()

    return render_template('search.html', users=users)

@app.route("/follow/<username>", methods=['POST'])
@login_required
def follow(username):
    if current_user.id == username:
        flash("You cannot follow yourself.", 'warning')
        return redirect(url_for('public_profile', username=username))

    print(f"username: {username}")
    user_to_follow = db.users.find_one({'username': username})
    print(f"user to follow: {user_to_follow}")

    if user_to_follow:
        # Update the current user's following list
        db.users.update_one(
            {'username': current_user.id},
            {'$addToSet': {'following': username}}
        )

        # Update the target user's followers list
        db.users.update_one(
            {'username': username},
            {'$addToSet': {'followers': current_user.id}}
        )

        flash(f"You are now following {username}.", 'success')
    else:
        flash("User not found.", 'danger')

    return redirect(url_for('public_profile', username=username))

@app.route("/unfollow/<username>", methods=['POST'])
@login_required
def unfollow(username):
    if current_user.id == username:
        flash("You cannot unfollow yourself.", 'warning')
        return redirect(url_for('public_profile', username=username))

    user_to_unfollow = db.users.find_one({'username': username})

    if user_to_unfollow:
        # Update the current user's following list to remove the user
        db.users.update_one(
            {'username': current_user.id},
            {'$pull': {'following': username}}
        )

        # Update the target user's followers list to remove the current user
        db.users.update_one(
            {'username': username},
            {'$pull': {'followers': current_user.id}}
        )

        flash(f"You are no longer following {username}.", 'success')
    else:
        flash("User not found.", 'danger')

    return redirect(url_for('public_profile', username=username))

if __name__ == "__main__":
    socketio.run(app, debug=True)