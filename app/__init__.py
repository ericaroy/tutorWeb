import os
from app.userlogic import grab_all_tutors
from flask_login import LoginManager
from app.forms.base_forms import TutorForm, LoginForm, RegistrationForm
from flask import Flask, render_template, request, redirect
from flask_admin import Admin

app = Flask(__name__)
admin = Admin(app, name='Tutor App', template_mode='bootstrap3')
the_login_manager = LoginManager()
the_login_manager.init_app(app)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/search')
def find_tutors():

	tutors = grab_all_tutors()
	return render_template('findtutors.html', tutors=tutors)


@app.route('/tutorapp', methods=['GET', 'POST'])
def tutorapp():

	form = TutorForm(request.form, csrf_enabled=False)

	return render_template('tutorapp.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form, csrf_enabled=False)

	return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

	form = RegistrationForm(request.form, csrf_enabled=False)

	return render_template('register.html', form=form)
