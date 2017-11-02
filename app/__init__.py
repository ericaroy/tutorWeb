import os
import pyrebase
import json
import requests
from app.userlogic import grab_all_tutors
from app.auth import authenticate_user, login_user
from app.forms.base_forms import TutorForm, LoginForm, RegistrationForm
from flask import Flask, render_template, request, redirect, url_for, \
 session, json, flash



app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# FIREBASE CONFIG
config = {

  "apiKey": os.environ['FIREBASE_SECRET_KEY'],
  "authDomain": "campustutors-78ccb.firebaseapp.com",
  "databaseURL": "https://campustutors-78ccb.firebaseio.com",
  "storageBucket": "campustutors-78ccb.appspot.com",
  "serviceAccount": "app/secret.json"
}

firebase = pyrebase.initialize_app(config)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/search')
def find_tutors():
    tutors = grab_all_tutors()
    return render_template('findtutors.html', tutors=tutors)


@app.route('/profile')
def get_profile():
    return render_template('profile.html')


@app.route('/tutorapp', methods=['GET', 'POST'])
def tutorapp():
    form = TutorForm(request.form, csrf_enabled=False)
    return render_template('tutorapp.html', form=form)


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
                # Load User


                print(user)
                print(account)

                session['logged_in'] = True
                session['user_token'] = user['idToken']

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
            auth = firebase.auth()
            db = firebase.database()
            user = auth.create_user_with_email_and_password(user_email, user_password)
            auth.send_email_verification(user['idToken'])

            data = {"email": user_email, "firstName": user_first_name, "isTutor": False, "lastName": user_last_name,
            "profileImage": '',
            "program": user_program, "subjects": ['None'], "isAdmin": False}
            db.child("users").child(user['localId']).set(data)

            return redirect(url_for('login'))




            return redirect('/')
    return render_template('register.html', form=form)
