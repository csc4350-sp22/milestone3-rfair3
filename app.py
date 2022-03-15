#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""
this is a file 
"""
import os
import random
import random
import flask

from flask import url_for, redirect, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv, find_dotenv
from wikipedia import get_wiki_link
from tmdb import get_movie_data


load_dotenv(find_dotenv())




app = flask.Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config[
        'SQLALCHEMY_DATABASE_URI'
        ].replace("postgres://","postgresql://")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None




#Table for username and password
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)

#Table for movie id, comments and ratings
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieid = db.Column(db.String(300), nullable=False)
    username = db.Column(db.String(300), nullable=False)
    comments = db.Column(db.String(300), nullable=False)
    rating =db.Column(db.String(300), nullable=False)


#Allows user to register using form
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "Opps. Someone already has that username. Please choose a different one.")



#Takes username and pw and compares 
class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[ InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


MOVIE_IDS = [
    10426, 
    12153, 
    584, 
    5174, 
    16555
]


@bp.route("/newcomment")
def newcomment():
    # NB: DO NOT add an "index.html" file in your normal templates folder
    # Flask will stop serving this React page correctly
    return flask.render_template("index.html")


#This route should fetch data from Comment API and display on react page
@bp.route("/comment_fetch", methods=["GET",'POST'])
def commentfetch():
    Comments = Comment.query.all()

    view_comments = []

    for c in Comments:
        view_comments.append({
            "movieid": c.movieid,
            "comments": c.comments,
            "username": c.username,
            "rating": c.rating,
        })
        print(view_comments)
        return jsonify({"Comments": view_comments})



@bp.route("/save_comments", methods=["GET",'POST'])
def savecomments():
    Comments = Comment.query.filter_by(username= current_user.username).all()

    edited_comments = flask.request.get_json()



    return("Your changes have been successfully saved", print(edited_comments))

    




#Login Users if account exists 
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('moviehp'))
    return flask.render_template("login.html", form=form)


   

#Register Users 
@app.route("/register", methods=['GET', 'POST'])
def register():
    form= RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data.encode('utf-8'))
        new_user = User(username=form.username.data, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return flask.render_template("register.html", form=form)



#Logout user after done commenting and viewing site 
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    

#Displays movies on website 
@app.route("/", methods=['GET', 'POST'])
@login_required
def moviehp():
    movie_id = random.choice(MOVIE_IDS)
    username= current_user.username
    # API calls
    (movieid, title, tagline, genre, poster_image) = get_movie_data(movie_id)
    wikipedia_url = get_wiki_link(title)
    if flask.request.method == "POST":
        data = flask.request.form
        new_comment = Comment(
            comments=data["comments"],
            username=data["username"],
            movieid=data["movieid"],
            rating=data["rating"]
        )
        db.session.add(new_comment)
        db.session.commit()

    comments = Comment.query.all()
    num_comments = len(comments)

    
    return flask.render_template(
        "moviehp.html",
        title=title,
        tagline=tagline,
        genre=genre,
        poster_image=poster_image,
        wiki_url=wikipedia_url,
        movieid=movieid,
        username=username,
        num_comments=num_comments,
        comments=comments,
    )


app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
