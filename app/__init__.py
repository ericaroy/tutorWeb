import os
from app.userlogic import grab_all_tutors
from flask_login import LoginManager
from app.forms.base_forms import TutorForm, LoginForm, RegistrationForm
from flask import Flask, render_template, request, redirect, url_for, session, json
from flask_admin import Admin
from flask_oauthlib.client import OAuth

app = Flask(__name__)
admin = Admin(app, name='Tutor App', template_mode='bootstrap3')
the_login_manager = LoginManager()
the_login_manager.init_app(app)
oauth = OAuth(app)
app.secret_key = os.environ['SECRET_KEY']

google = oauth.remote_app(
    'google',
    consumer_key=os.environ['GOOGLE_CLIENT_ID'],
    consumer_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
	if 'google_token' in session:
		me = google.get('userinfo')
		x = json.dumps(me.data)
		f = json.loads(x)

		return render_template('index.html', f=f)
	return render_template('index.html')


@app.route('/search')
def find_tutors():

	tutors = grab_all_tutors()
	return render_template('findtutors.html', tutors=tutors)


@app.route('/profile')
def get_profile():
	if 'google_token' in session:
		me = google.get('userinfo')
		x = json.dumps(me.data)
		f = json.loads(x)
	return render_template('profile.html',f=f)


@app.route('/tutorapp', methods=['GET', 'POST'])
def tutorapp():

	form = TutorForm(request.form, csrf_enabled=False)

	return render_template('tutorapp.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':

		return google.authorize(callback=url_for('authorized', _external=True))


	#Check Firebase to see if there is already an account before creating, if so pass
	return render_template('index')


@app.route('/logout')
def logout():
	session.pop('google_token', None)
	return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')

    return redirect(url_for('index', me=me))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/register', methods=['GET', 'POST'])
def register():

	form = RegistrationForm(request.form, csrf_enabled=False)

	return render_template('register.html', form=form)
