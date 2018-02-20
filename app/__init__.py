import os
import pyrebase
import json
import requests
import time
from datetime import date
from functools import wraps
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed
from flask_admin import Admin, AdminIndexView, expose
from app.userlogic import grab_all_tutors, grab_tutor_applications
from app.auth import authenticate_user, login_user
from app.forms.base_forms import TutorForm, LoginForm, RegistrationForm, AddTutorForm
from flask import Flask, render_template, request, redirect, url_for, \
 session, json, flash, Response


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
admin = Admin(app, name='CampusTutors', template_mode='bootstrap3')
admin_permission = Permission(RoleNeed('admin'))
# FIREBASE CONFIG
config = {

  "apiKey": os.environ['FIREBASE_SECRET_KEY'],
  "authDomain": "campustutors-78ccb.firebaseapp.com",
  "databaseURL": "https://campustutors-78ccb.firebaseio.com",
  "storageBucket": "campustutors-78ccb.appspot.com",
  "serviceAccount": "app/secret.json"
}

firebase = pyrebase.initialize_app(config)
principals = Principal(app)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/search')
def find_tutors():

    tutors = grab_all_tutors()

    return render_template('findtutors.html', tutors=tutors)


@app.route('/profile')
@login_required
def get_profile():
    # Grab User by username/Display Profile only if Auth = Current User Auth

    applications = grab_tutor_applications()
    department_tutors = grab_all_tutors()

    return render_template('profile.html', applications=applications, department_tutors=department_tutors)

# Refactor login, register, tutorapp instead of multiple calls to DB


def send_simple_message(body, subject):

    return requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(os.environ['MAILGUN_DOMAIN']),
        auth=("api", os.environ['MAILGUN_PRIVATE_KEY']),
        data={"from": "enroy@ualr.edu",
              "to": 'enroy@ualr.edu',
              "subject": subject,
              "text": body,
              "html": render_template('TutorApplication.html', body=body)
              })


@app.route('/tutorapp', methods=['GET', 'POST'])
@login_required
def tutorapp():

        form = TutorForm(request.form, csrf_enabled=False)

        if request.method == 'POST':
            if form.validate_on_submit():

                user_name = session['user_first_name'] + " " + session['user_last_name']
                user_phone = form.phone.data
                user_t_number = form.tnumber.data
                user_gpa = str(form.gpa.data)
                user_main_subject = form.subjects.data
                today = date.today()
                today = str(today)

                db = firebase.database()

                data = {"name": user_name, "application_date": today, "gpa": user_gpa, "t_number": user_t_number, "phone": user_phone, "email": session['email'], "approved": False, "subject": user_main_subject, "program": session['program']}
                db.child("tutorapplications").child(session['user_id']).set(data)
                body = data
                subject = 'New Tutor Application'
                send_simple_message(body, subject)
                flash('Application Sent')

                return redirect(url_for('get_profile'))

        return render_template('tutorapp.html', form=form)


@app.route('/addtutor', methods=['GET', 'POST'])
@login_required
def addtutorapp():
    form = AddTutorForm(request.form, csrf_enabled=False)

    if request.method == 'POST':
        if form.validate_on_submit():
            user_name = form.username.data
            user_password = form.password.data
            user_email = form.email.data
            user_first_name = form.firstName.data
            user_last_name = form.lastName.data
            user_phone = form.phone.data
            user_main_subject = form.subjects.data
            auth = firebase.auth()
            db = firebase.database()
            user = auth.create_user_with_email_and_password(user_email, user_password)

            data = {"firstName": user_first_name, "lastName": user_last_name, "gpa": '', "t_number": '',
                    "phone": user_phone, "email": user_email, "profileImage": '', "role": 'tutor', "isTutor": True, "isTutorVerified": True, "subjects": [user_main_subject],
                    "program": session['program']}
            db.child("users").child(user['localId']).set(data)

    return render_template('addtutor.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_email = form.email.data
                user_password = form.password.data

                auth = firebase.auth()
                db = firebase.database()
                user = auth.sign_in_with_email_and_password(user_email, user_password)
                account = auth.get_account_info(user['idToken'])

                # Verify Firebase DB User Account
                '''
                if account['users'][0]['emailVerified'] is False:
                    flash('Your email is not verified, click here to resend', 'error')
                    auth.send_email_verification(user['idToken'])
                '''
                # Load User from DB & into Login-Manager
                b = db.child("users").child(user['localId']).get()

                session['logged_in'] = True
                session['user_token'] = user['idToken']
                session['user_id'] = user['localId']
                session['user_first_name'] = b.val()['firstName']
                session['user_last_name'] = b.val()['lastName']
                session['role'] = b.val()['role']
                session['email'] = b.val()['email']
                session['program'] = b.val()['program']


                return redirect('/')

            except requests.exceptions.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                if error == 'EMAIL_NOT_FOUND':
                    flash('Email Not Found. Please Register an Account.', 'error')
                else:
                    flash(error)

        else:
            pass

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_token', None)
    session.pop('user_first_name', None)
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():

            user_email = form.email.data
            user_password = form.password.data
            user_first_name = form.firstName.data
            user_last_name = form.lastName.data
            user_program = form.program.data
            user_name = form.username.data
            auth = firebase.auth()
            db = firebase.database()
            user = auth.create_user_with_email_and_password(user_email, user_password)
            auth.send_email_verification(user['idToken'])
            data = {"email": user_email, "firstName": user_first_name, "role": 'user', "lastName": user_last_name,
            "userName": user_name, "profileImage": '',
            "program": user_program, "subjects": ['None'], "isTutorVerified": False, "isTutor": False}
            db.child("users").child(user['localId']).set(data)

            return redirect(url_for('login'))

            #return redirect('/')
    return render_template('register.html', form=form)

