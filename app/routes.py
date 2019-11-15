from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app.forms import LoginForm
from app.models import User
from werkzeug.urls import url_parse


# route to index
@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    :return: render template with our HTML
    :rtype: render_template
    """
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


# route to login page
# accept both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, redirect to the index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # query the User database for the user matching the username in the form
        # .first() only gets the first result of the query since usernames are unique!
        user = User.query.filter_by(username=form.username.data).first()
        # if username is invalid or password check fails, flash error
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            # then redirect to login screen
            return redirect(url_for('login'))
        # if username and password check succeeds, login user (set user to current_user)
        login_user(user, remember=form.remember_me.data)
        # after user is logged in, determine which page to pass them to
        next_page = request.args.get('next')
        # if there is no next_page, user is redirected to index
        # url_parse checks that next_page is a relative location and not an absolute path
        # this prevents attackers from inserting a foreign URL
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # redirect user to next_page based on above logic
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# route to logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
