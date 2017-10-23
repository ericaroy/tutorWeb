from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextField, validators


class TutorForm(FlaskForm):

    firstName = StringField('First Name',[validators.Length(min=4, max=40),
                                                  validators.Regexp('[A-Za-z0-9]+',
                                                                    message="Please enter your first name")], render_kw={'placeholder': 'First Name'})

    lastName = StringField('Last Name',[validators.Length(min=3, max=40),
                                                        validators.Regexp('[A-Za-z0-9]+',
                                                                          message="Please enter your last name")], render_kw={'placeholder':'Last Name'})

    email = StringField('Email',[validators.Length(min=3, max=15),
                                                        validators.Regexp('[A-Za-z0-9]+',
                                                                          message="Please enter your email address")], render_kw={'placeholder':'University Email'})
    phone = TextField('Phone Number',[validators.Length(min=3, max=10),
                                                            validators.Regexp('[0-9]+',
                                                                              message="Please enter your phone number")], render_kw={'placeholder':'Phone Number'})
    tnumber = TextField('T-Number',[validators.Length(min=3, max=10),
                                                            validators.Regexp('[0-9]+',
                                                                              message="Please enter your T-Number")], render_kw={'placeholder':'T-Number'})
    gpa = TextField('GPA',[validators.Length(min=1, max=3),
                                                            validators.Regexp('[0-9]+',
                                                                              message="Please enter your Overall GPA")], render_kw={'placeholder':'GPA'})

    program = SelectField(u'Program', choices=[('USS', 'USS Tutors'), ('SS', 'Student Success'), ('math', 'Math Tutors'), ('trio', 'TRiO')])

    subjects = SelectField(u'Main Subject', choices=[('MATH', 'Math'), ('ACCT', 'Accounting'), ('AC', 'Applied Communication'), ('SCIENCE', 'Science'), ('GENERAL', 'General')])


class LoginForm(FlaskForm):

    email = StringField('Email',[validators.Length(min=3, max=15),
                                                        validators.Regexp('[A-Za-z0-9]+',
                                                                          message="Please enter your email address")], render_kw={'placeholder':'University Email'})
    password = TextField('Phone Number',[validators.Length(min=3, max=10),
                                                            validators.Regexp('[A-Za-z0-9]+',
                                                                              message="Please enter your password")], render_kw={'placeholder':'Phone Number'})

class RegistrationForm(FlaskForm):

    firstName = StringField('First Name',[validators.Length(min=4, max=40),
                                                  validators.Regexp('[A-Za-z0-9]+',
                                                                    message="Please enter your first name")], render_kw={'placeholder': 'First Name'})

    lastName = StringField('Last Name',[validators.Length(min=3, max=40),
                                                        validators.Regexp('[A-Za-z0-9]+',
                                                                          message="Please enter your last name")], render_kw={'placeholder':'Last Name'})

    email = StringField('Email',[validators.Length(min=3, max=15),
                                                        validators.Regexp('[A-Za-z0-9]+',
                                                                          message="Please enter your email address")], render_kw={'placeholder':'University Email'})
