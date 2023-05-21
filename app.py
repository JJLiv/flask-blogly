"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jerm'

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def user_listing():
    '''redirect to users route'''
    # users = User.query.all()
    return redirect('/users')

@app.route('/users')
def list_users():
    """show all users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/new-users', methods='GET')
def add_user_form():
    """show form"""
    return render_template('new-user.html')

@app.route("/new-users", methods=["POST"])
def users_new():
    """submit form"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        img_url=request.form['img_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show a single user"""
    user = User.query.get_or_404(user_id)

    return render_template('show-user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def user_edit_update(user_id):
    """handle form submission"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')