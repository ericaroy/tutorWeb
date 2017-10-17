import os
import app.firebaseAuth
from app.forms.tutorForm import TutorForm
from flask import Flask, render_template, request, redirect
from flask_admin import Admin

app = Flask(__name__)
admin = Admin(app, name='Tutor App', template_mode='bootstrap3')


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/search')
def find_tutors():
	return render_template('findtutors.html')


@app.route('/tutorapp', methods=['GET', 'POST'])
def tutorapp():

	form = TutorForm(request.form, csrf_enabled=False)

	return render_template('tutorapp.html', form=form)
