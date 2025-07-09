from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, FloatField
from wtforms.validators import DataRequired, Email
from datetime import datetime
import threading, webbrowser, time
from jinja2 import DictLoader
from wtforms.widgets import ListWidget, CheckboxInput
from flask import send_from_directory
from wtforms import SelectField
from wtforms import StringField, SubmitField, SelectMultipleField, FloatField, SelectField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Optional
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask import jsonify
from wtforms import SelectField, DateTimeLocalField, TextAreaField, SubmitField
import os
from wtforms.validators import DataRequired

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'

app.config['SECRET_KEY'] = 'secure-secret-key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), default='client')  # default as client

    doctor = db.relationship('Doctor', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    description = db.Column(db.Text)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    poster = db.relationship('User', backref='jobs')



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    message_type = db.Column(db.String(50), default='general')  # <-- NEW FIELD

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')
    job = db.relationship('Job', backref='messages')
    doctor = db.relationship('Doctor', backref='messages')


# Doctor Registration Form (For Admin)
class DoctorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Doctor')

# Job Posting Form (For User)
class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Job')

# Database Models Updates

class ClientRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Client')




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# Models
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='doctor')

    position = db.Column(db.String(10), nullable=False)
    specialty = db.Column(db.String(100))
    subspecialty = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    alt_phone = db.Column(db.String(20))
    city_of_residence = db.Column(db.String(100))
    medical_school = db.Column(db.String(100))
    med_grad_month_year = db.Column(db.String(20))
    residency = db.Column(db.String(100))
    residency_grad_month_year = db.Column(db.String(20))
    fellowship = db.Column(db.Text)
    fellowship_grad_month_year = db.Column(db.Text)
    bachelors = db.Column(db.String(100))
    bachelors_grad_month_year = db.Column(db.String(20))
    msn = db.Column(db.String(100))
    msn_grad_month_year = db.Column(db.String(20))
    dnp = db.Column(db.String(100))
    dnp_grad_month_year = db.Column(db.String(20))
    additional_training = db.Column(db.Text)
    sponsorship_needed = db.Column(db.Boolean)
    malpractice_cases = db.Column(db.Text)
    certification = db.Column(db.String(30))
    emr = db.Column(db.String(100))
    languages = db.Column(db.String(200))
    states_licensed = db.Column(db.Text)
    states_willing_to_work = db.Column(db.Text)
    salary_expectations = db.Column(db.Float)
    joined = db.Column(db.DateTime, default=datetime.utcnow)







class ScheduledCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    scheduled_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    canceled = db.Column(db.Boolean, default=False)
    reschedule_requested = db.Column(db.Boolean, default=False)
    reschedule_note = db.Column(db.String(255), nullable=True)
    reschedule_datetime = db.Column(db.DateTime, nullable=True)
    invite_status = db.Column(db.String(20), default="Pending") # New: Pending/Accepted/Declined

    # CRUCIAL FIX (MUST MATCH EXACTLY)
    doctor = db.relationship('Doctor', backref=db.backref('scheduled_calls', lazy=True))
    
    scheduled_by = db.relationship('User', backref=db.backref('scheduled_calls_scheduled', lazy=True))
    job = db.relationship('Job', backref='scheduled_calls') 

    def __repr__(self):
        return f'<ScheduledCall {self.id} with Doctor {self.doctor_id}>'






class MalpracticeCaseForm(FlaskForm):
    incident_year = StringField('Incident Year')
    outcome = SelectField(
        'Outcome',
        choices=[('Dropped', 'Dropped'), ('Won', 'Won'), ('Settled/Lost', 'Settled/Lost')],
        validators=[Optional()]
    )
    payout_amount = FloatField('Payout Amount', validators=[Optional()])

    class Meta:
        csrf = False

# Forms
class DoctorForm(FlaskForm):
    position = SelectField('Position', choices=[('MD','MD'),('DO','DO'),('NP','NP'),('PA','PA')], validators=[DataRequired()])
    specialty = StringField('Specialty', validators=[DataRequired()])
    subspecialty = StringField('Subspecialty', validators=[Optional()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    alt_phone = StringField('Alternative Phone Number', validators=[Optional()])
    city_of_residence = StringField('City of Residence', validators=[Optional()])

    # MD/DO fields
    medical_school = StringField('Medical School', validators=[Optional()])
    med_grad_month_year = StringField('Medical Graduation (Month/Year)', validators=[Optional()])
    residency = StringField('Residency', validators=[Optional()])
    residency_grad_month_year = StringField('Residency Graduation (Month/Year)', validators=[Optional()])
    fellowship = FieldList(StringField('Fellowship'), min_entries=1)
    fellowship_grad_month_year = FieldList(StringField('Fellowship Graduation (Month/Year)'), min_entries=1)

    # NP/PA fields
    bachelors = StringField('Bachelors Degree', validators=[Optional()])
    bachelors_grad_month_year = StringField('Bachelors Graduation (Month/Year)', validators=[Optional()])
    msn = StringField('Masters of Science in Nursing', validators=[Optional()])
    msn_grad_month_year = StringField('MSN Graduation (Month/Year)', validators=[Optional()])
    dnp = StringField('Doctor of Nursing', validators=[Optional()])
    dnp_grad_month_year = StringField('DNP Graduation (Month/Year)', validators=[Optional()])
    additional_training = StringField('Additional Training', validators=[Optional()])
    sponsorship_needed = BooleanField('Sponsorship Needed?', validators=[Optional()])

    malpractice_cases = FieldList(FormField(MalpracticeCaseForm), min_entries=1, max_entries=15)

    certification = SelectField(
    'Certification',
    choices=[
        ('Board Certified', 'Board Certified'),
        ('Board Eligible', 'Board Eligible'),
        ('Not Boarded', 'Not Boarded')
    ],
    validators=[Optional()]
    )

    emr = StringField('EMR', validators=[Optional()])
    languages = StringField('Languages', validators=[Optional()])

    states_licensed = SelectMultipleField('States Licensed', choices=[(state,state) for state in states], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    states_willing_to_work = SelectMultipleField('States Willing to Work', choices=[(state,state) for state in states], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    salary_expectations = FloatField('Salary Expectations', validators=[Optional()])

    submit = SubmitField('Submit')

class ScheduledCallForm(FlaskForm):
    doctor_id = SelectField('Doctor', validators=[DataRequired()])
    datetime = DateTimeLocalField('Call Date & Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    reason = TextAreaField('Reason for Call', validators=[DataRequired()])
    submit = SubmitField('Schedule Call')
# Add this clearly above your route definitions:

app.jinja_loader = DictLoader({
    'base.html': '''
    <!doctype html>
    <html lang="en">
    <head>
        <title>Healthcare Systems</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.13/flatpickr.min.css">

        <!-- FullCalendar CSS -->
        <link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.css' rel='stylesheet' />

        <!-- FullCalendar JS -->
        <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>
        <style>
            body {
                background-color: #f8f9fa;
            }

            .form-control, .form-select {
                border-radius: 8px;
                border: 1px solid #ced4da;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                padding: 10px;
                transition: all 0.3s ease;
            }

            .form-control:focus, .form-select:focus {
                border-color: #004080;
                box-shadow: 0 0 0 0.2rem rgba(0, 64, 128, 0.25);
            }

            label {
                font-weight: 600;
                color: #333;
            }

            .btn {
                padding: 10px 15px;
                border-radius: 6px;
            }

            .form-check-input {
                transform: scale(1.2);
                margin-right: 8px;
            }

            .form-check-label {
                font-weight: normal;
            }

            .border {
                border: 1px solid #dee2e6 !important;
            }

            h4 {
                margin-top: 20px;
                padding-bottom: 8px;
                border-bottom: 2px solid #004080;
                margin-bottom: 15px;
            }
        </style>
    </head>
    <body class="bg-light">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow">
            <div class="container">
                <a class="navbar-brand d-flex align-items-center" href="{{ url_for('dashboard') }}">
                    <img src="{{ url_for('static', filename='secondimagebeca2.png') }}" 
                         alt="Logo" 
                         style="height: 100px !important; width: auto !important;">
                    Healthcare Systems
                </a>
                <div class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        {% set unread_count = current_user.received_messages|selectattr('read', 'equalto', False)|list|length %}
                        {% if current_user.role == 'doctor' %}
                            <a class="nav-link text-white" href="{{ url_for('doctor_dashboard') }}">Dashboard</a>
                            <a class="nav-link text-white" href="{{ url_for('doctor_edit_profile') }}">Edit Profile</a>
                            <a class="nav-link text-white" href="{{ url_for('doctor_jobs') }}">Jobs</a>
                            <a class="nav-link text-white position-relative" href="{{ url_for('doctor_inbox') }}">
                                Inbox
                                {% if unread_count > 0 %}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ unread_count }}
                                </span>
                                {% endif %}
                            </a>
                            <a class="nav-link text-white" href="{{ url_for('logout') }}">Logout</a>

                        {% elif current_user.role == 'admin' %}
                            <a class="nav-link text-white" href="{{ url_for('register_doctor') }}">Create Doctor Login</a>
                            <a class="nav-link text-white" href="{{ url_for('register_client') }}">Create Client Login</a>
                            <a class="nav-link text-white" href="{{ url_for('add_doctor') }}">Add Doctor</a>
                            <a class="nav-link text-white" href="{{ url_for('doctors') }}">View Doctors</a>
                            <a class="nav-link text-white" href="{{ url_for('post_job') }}">Post Job</a>
                            <a class="nav-link text-white position-relative" href="{{ url_for('admin_inbox') }}">
                                Inbox
                                {% if unread_count > 0 %}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ unread_count }}
                                </span>
                                {% endif %}
                            </a>
                            <a class="nav-link text-white" href="{{ url_for('logout') }}">Logout</a>

                        {% elif current_user.role == 'client' %}
                            <a class="nav-link text-white" href="{{ url_for('post_job') }}">Post Job</a>
                            <a class="nav-link text-white" href="{{ url_for('client_my_jobs') }}">My Jobs</a>
                            <a class="nav-link text-white" href="{{ url_for('schedule_call') }}">Schedule Call</a>
                            <a class="nav-link text-white" href="{{ url_for('calls') }}">Scheduled Calls</a>
                            <a class="nav-link text-white" href="{{ url_for('doctors') }}">View Doctors</a>
                            <a class="nav-link text-white position-relative" href="{{ url_for('client_inbox') }}">
                                Inbox
                                {% if unread_count > 0 %}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ unread_count }}
                                </span>
                                {% endif %}
                            </a>
                            <a class="nav-link text-white" href="{{ url_for('logout') }}">Logout</a>

                        {% else %}
                            <a class="nav-link text-white" href="{{ url_for('logout') }}">Logout</a>
                        {% endif %}
                    {% else %}
                        <a class="nav-link text-white" href="{{ url_for('login') }}">Login</a>
                    {% endif %}
                </div>



            </div>
        </nav>
        <div class="container py-4">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% for category, msg in messages %}
                    <div class="alert alert-{{ category }}">{{ msg }}</div>
                {% endfor %}
            {% endwith %}
            {% block content %}{% endblock %}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
        <script>
            flatpickr("#datetime", {enableTime: true, dateFormat: "Y-m-d\\TH:i"});
        </script>
    </body>
    </html>
    ''',


    'index.html': '''{% extends "base.html" %}{% block content %}
        <h1>Beca Staffing CRM Dashboard</h1>
        <a class="btn btn-success" href="/add_doctor">Add Doctor</a>
        <a class="btn btn-info" href="/schedule_call">Schedule Call with Doctor</a>
        <a class="btn btn-primary" href="/calls">View Scheduled Calls</a>
        <a class="btn btn-secondary" href="/doctors">View Doctors</a>
    {% endblock %}''',

    'login.html': '''{% extends "base.html" %}
    {% block content %}
        <h2>Login</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            <div class="mb-3">
                {{ form.username.label }} {{ form.username(class="form-control") }}
            </div>
            <div class="mb-3">
                {{ form.password.label }} {{ form.password(class="form-control", type="password") }}
            </div>
            {{ form.submit(class="btn btn-primary") }}
        </form>
        {% endblock %}''',

    'client_dashboard.html': '''
        {% extends 'base.html' %}

        {% block content %}
        <h2>Client Dashboard</h2>

        <div class="mb-3">
            <a class="btn btn-success" href="{{ url_for('schedule_call') }}">Schedule Call</a>
            <a class="btn btn-primary" href="{{ url_for('calls') }}">Scheduled Calls</a>
            <a class="btn btn-secondary" href="{{ url_for('doctors') }}">View Doctors</a>
            <a class="btn btn-info" href="{{ url_for('client_inbox') }}">Inbox</a>
            <a class="btn btn-warning" href="{{ url_for('post_job') }}">Post Job</a>
            <a class="btn btn-dark" href="{{ url_for('client_my_jobs') }}">My Jobs</a>
        </div>

        <div id='calendar'></div>

        <div class="mt-4">
            <h3>Reschedule Requests</h3>
            {% if reschedule_requests %}
                <ul class="list-group">
                {% for request in reschedule_requests %}
                    <li class="list-group-item">
                        Doctor: Dr. {{ request.doctor.first_name }} {{ request.doctor.last_name }}<br>
                        Original: {{ request.datetime.strftime('%Y-%m-%d %H:%M') }}<br>
                        Requested: {{ request.reschedule_datetime.strftime('%Y-%m-%d %H:%M') }}<br>
                        Reason: {{ request.reschedule_note }}<br>

                        <form action="{{ url_for('client_handle_reschedule', call_id=request.id) }}" method="post">
                            <textarea name="client_note" class="form-control mt-2" placeholder="Optional note"></textarea>
                            <button type="submit" name="action" value="accept" class="btn btn-success mt-2">Accept</button>
                            <button type="submit" name="action" value="decline" class="btn btn-danger mt-2">Decline</button>
                        </form>
                    </li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No reschedule requests at this time.</p>
            {% endif %}
        </div>

        <script>
        document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                height: 650,
                events: {{ events | tojson }},
                eventDidMount: function(info) {
                    // Tooltip to show event status on hover
                    let tooltip = new bootstrap.Tooltip(info.el, {
                        title: info.event.extendedProps.status,
                        placement: 'top',
                        trigger: 'hover',
                        container: 'body'
                    });

                    // Strikethrough canceled events
                    if (info.event.extendedProps.status === 'Canceled') {
                        info.el.style.textDecoration = 'line-through';
                    }
                },
                eventClick: function(info) {
                    window.location.href = "/edit_call/" + info.event.id;
                }
            });
            calendar.render();
        });
        </script>

        <!-- Include Bootstrap Tooltip -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

        {% endblock %}''',




    'register_doctor.html' : '''{% extends "base.html" %}
    {% block content %}
        <h2>Create Doctor Account</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            {{ form.username.label }} {{ form.username(class="form-control") }}
            {{ form.email.label }} {{ form.email(class="form-control") }}
            {{ form.password.label }} {{ form.password(class="form-control") }}
            {{ form.submit(class="btn btn-primary mt-3") }}
        </form>
        {% endblock %}''',
    
    'post_job.html': '''{% extends "base.html" %}
    {% block content %}
        <h2>Post a New Job</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            {{ form.title.label }} {{ form.title(class="form-control") }}
            {{ form.location.label }} {{ form.location(class="form-control") }}
            {{ form.salary.label }} {{ form.salary(class="form-control") }}
            {{ form.description.label }} {{ form.description(class="form-control") }}
            {{ form.submit(class="btn btn-success mt-3") }}
            <a href="{{ url_for('scrape_jobs') }}" class="btn btn-warning mt-3">Scrape Jobs from DocCafe</a>
        </form>
        {% endblock %}''',

    'register.html': '''{% extends "base.html" %}
    {% block content %}
        <h2>Register New User</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            <div class="mb-3">
                {{ form.username.label }} {{ form.username(class="form-control") }}
            </div>
            <div class="mb-3">
                {{ form.password.label }} {{ form.password(class="form-control", type="password") }}
            </div>
            {{ form.submit(class="btn btn-success") }}
        </form>
        {% endblock %}''',

    'add_doctor.html': '''{% extends "base.html" %}{% block content %}
        <h2>Add Doctor</h2>
        <form method="post">
            {{ form.hidden_tag() }}

            <div class="mb-3">{{ form.position.label }} {{ form.position(class="form-select", id="position") }}</div>
            <div class="mb-3">{{ form.specialty.label }} {{ form.specialty(class="form-control") }}</div>
            <div class="mb-3">{{ form.subspecialty.label }} {{ form.subspecialty(class="form-control") }}</div>
            <div class="mb-3">{{ form.first_name.label }} {{ form.first_name(class="form-control") }}</div>
            <div class="mb-3">{{ form.last_name.label }} {{ form.last_name(class="form-control") }}</div>
            <div class="mb-3">{{ form.email.label }} {{ form.email(class="form-control") }}</div>
            <div class="mb-3">{{ form.phone.label }} {{ form.phone(class="form-control") }}</div>
            <div class="mb-3">{{ form.alt_phone.label }} {{ form.alt_phone(class="form-control") }}</div>
            <div class="mb-3">{{ form.city_of_residence.label }} {{ form.city_of_residence(class="form-control") }}</div>

            <div id="md_do_fields" style="display:none;">
                <h4>MD/DO Information</h4>
                <div class="mb-3">{{ form.medical_school.label }} {{ form.medical_school(class="form-control") }}</div>
                <div class="mb-3">{{ form.med_grad_month_year.label }} {{ form.med_grad_month_year(class="form-control") }}</div>
                <div class="mb-3">{{ form.residency.label }} {{ form.residency(class="form-control") }}</div>
                <div class="mb-3">{{ form.residency_grad_month_year.label }} {{ form.residency_grad_month_year(class="form-control") }}</div>

                <div id="fellowship_fields">
                    {% for fellowship_field in form.fellowship %}
                        <div class="mb-3">{{ fellowship_field.label }} {{ fellowship_field(class="form-control") }}</div>
                    {% endfor %}
                    {% for fellowship_date_field in form.fellowship_grad_month_year %}
                        <div class="mb-3">{{ fellowship_date_field.label }} {{ fellowship_date_field(class="form-control") }}</div>
                    {% endfor %}
                </div>
            </div>

            <div id="np_pa_fields" style="display:none;">
                <h4>NP/PA Information</h4>
                <div class="mb-3">{{ form.bachelors.label }} {{ form.bachelors(class="form-control") }}</div>
                <div class="mb-3">{{ form.bachelors_grad_month_year.label }} {{ form.bachelors_grad_month_year(class="form-control") }}</div>
                <div class="mb-3">{{ form.msn.label }} {{ form.msn(class="form-control") }}</div>
                <div class="mb-3">{{ form.msn_grad_month_year.label }} {{ form.msn_grad_month_year(class="form-control") }}</div>
                <div class="mb-3">{{ form.dnp.label }} {{ form.dnp(class="form-control") }}</div>
                <div class="mb-3">{{ form.dnp_grad_month_year.label }} {{ form.dnp_grad_month_year(class="form-control") }}</div>
                <div class="mb-3">{{ form.additional_training.label }} {{ form.additional_training(class="form-control") }}</div>
                <div class="form-check mb-3">{{ form.sponsorship_needed(class="form-check-input") }} {{ form.sponsorship_needed.label(class="form-check-label") }}</div>
            </div>

            <h4>Certification & Additional Information</h4>
            <div class="mb-3">{{ form.certification.label }} {{ form.certification(class="form-select") }}</div>
            <div class="mb-3">{{ form.emr.label }} {{ form.emr(class="form-control") }}</div>
            <div class="mb-3">{{ form.languages.label }} {{ form.languages(class="form-control") }}</div>

            <h4>Malpractice Cases</h4>
            <div id="malpractice_fields">
                {% for case in form.malpractice_cases %}
                    <div class="border p-3 mb-3 rounded">
                        <div class="mb-2">{{ case.incident_year.label }} {{ case.incident_year(class="form-control") }}</div>
                        <div class="mb-2">{{ case.outcome.label }} {{ case.outcome(class="form-select") }}</div>
                        <div class="mb-2">{{ case.payout_amount.label }} {{ case.payout_amount(class="form-control") }}</div>
                    </div>
                {% endfor %}
            </div>

            <div class="mb-3">
                <label>{{ form.states_licensed.label }}</label>
                {% for state in form.states_licensed %}
                    <div class="form-check">{{ state }} {{ state.label }}</div>
                {% endfor %}
            </div>

            <div class="mb-3">
                <label>{{ form.states_willing_to_work.label }}</label>
                {% for state in form.states_willing_to_work %}
                    <div class="form-check">{{ state }} {{ state.label }}</div>
                {% endfor %}
            </div>

            <div class="mb-3">{{ form.salary_expectations.label }} {{ form.salary_expectations(class="form-control") }}</div>

            {{ form.submit(class="btn btn-primary") }}
        </form>

        <script>
            document.addEventListener('DOMContentLoaded', () => {
                const positionField = document.getElementById('position');
                const md_do_fields = document.getElementById('md_do_fields');
                const np_pa_fields = document.getElementById('np_pa_fields');

                function toggleFields() {
                    const val = positionField.value;
                    md_do_fields.style.display = ['MD', 'DO'].includes(val) ? 'block' : 'none';
                    np_pa_fields.style.display = ['NP', 'PA'].includes(val) ? 'block' : 'none';
                }

                positionField.addEventListener('change', toggleFields);
                toggleFields();  
            });
        </script>
    {% endblock %}''',

    'client_my_jobs.html': '''{% extends "base.html" %}
    {% block content %}
        <h2>My Job Postings</h2>
        {% if jobs %}
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Location</th>
                        <th>Salary</th>
                        <th>Edit</th>
                    </tr>
                </thead>
                <tbody>
                    {% for job in jobs %}
                    <tr>
                        <td>{{ job.title }}</td>
                        <td>{{ job.location }}</td>
                        <td>{{ job.salary }}</td>
                        <td>
                            <a href="{{ url_for('edit_job', job_id=job.id) }}" class="btn btn-warning btn-sm">Edit</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p>You haven't posted any jobs yet.</p>
        {% endif %}
    {% endblock %}''',

    'schedule_call.html': '''
        {% extends "base.html" %}
        {% block content %}
            <h2>Schedule Call with Doctor</h2>
            <form method="post">
                {{ form.hidden_tag() }}

                <div class="mb-3">
                    {{ form.doctor_id.label }}
                    {{ form.doctor_id(class="form-select") }}
                </div>

                <div class="mb-3">
                    {{ form.datetime.label }}
                    {{ form.datetime(class="form-control", id="datetime") }}
                </div>

                <div class="mb-3">
                    {{ form.reason.label }}
                    {{ form.reason(class="form-control") }}
                </div>

                {{ form.submit(class="btn btn-primary") }}

                <div class="mt-3">
                    <button name="send_invite" value="yes" class="btn btn-info">Send Invite to Doctor</button>
                </div>
            </form>


            <!-- Include Select2 CSS and JS -->
            <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>

            <script>
                $(document).ready(function() {
                    $('.form-select').select2({
                        placeholder: "Select Doctor (Name | Email | Specialty)",
                        allowClear: true,
                        width: '100%'
                    });
                });
            </script>
        {% endblock %}''',

    'doctor_profile.html': '''{% extends "base.html" %}{% block content %}
        <h2>Doctor Profile: {{ doctor.first_name }} {{ doctor.last_name }}</h2>
        <div class="card shadow p-4 mb-4">
            <h5 class="card-title text-primary">Basic Information</h5>
            <p><strong>Position:</strong> {{ doctor.position }}</p>
            <p><strong>Specialty:</strong> {{ doctor.specialty }}</p>
            <p><strong>Subspecialty:</strong> {{ doctor.subspecialty }}</p>
            <p><strong>Email:</strong> {{ doctor.email }}</p>
            <p><strong>Phone:</strong> {{ doctor.phone }}</p>
            <p><strong>Alternative Phone:</strong> {{ doctor.alt_phone }}</p>
            <p><strong>City of Residence:</strong> {{ doctor.city_of_residence }}</p>
        </div>

        {% if doctor.medical_school %}
        <div class="card shadow p-4 mb-4">
            <h5 class="card-title text-primary">MD/DO Education</h5>
            <p><strong>Medical School:</strong> {{ doctor.medical_school }}</p>
            <p><strong>Graduation:</strong> {{ doctor.med_grad_month_year }}</p>
            <p><strong>Residency:</strong> {{ doctor.residency }}</p>
            <p><strong>Residency Graduation:</strong> {{ doctor.residency_grad_month_year }}</p>
            <p><strong>Fellowships:</strong> {{ doctor.fellowship }}</p>
            <p><strong>Fellowship Graduation:</strong> {{ doctor.fellowship_grad_month_year }}</p>
        </div>
        {% endif %}

        {% if doctor.bachelors %}
        <div class="card shadow p-4 mb-4">
            <h5 class="card-title text-primary">NP/PA Education</h5>
            <p><strong>Bachelors Degree:</strong> {{ doctor.bachelors }}</p>
            <p><strong>Bachelors Graduation:</strong> {{ doctor.bachelors_grad_month_year }}</p>
            <p><strong>MSN:</strong> {{ doctor.msn }}</p>
            <p><strong>MSN Graduation:</strong> {{ doctor.msn_grad_month_year }}</p>
            <p><strong>DNP:</strong> {{ doctor.dnp }}</p>
            <p><strong>DNP Graduation:</strong> {{ doctor.dnp_grad_month_year }}</p>
            <p><strong>Additional Training:</strong> {{ doctor.additional_training }}</p>
            <p><strong>Sponsorship Needed:</strong> {{ 'Yes' if doctor.sponsorship_needed else 'No' }}</p>
        </div>
        {% endif %}

        <div class="card shadow p-4 mb-4">
            <h5 class="card-title text-primary">Licensing & Work Preferences</h5>
            <p><strong>Certification:</strong> {{ doctor.certification }}</p>
            <p><strong>EMR:</strong> {{ doctor.emr }}</p>
            <p><strong>Languages:</strong> {{ doctor.languages }}</p>
            <p><strong>States Licensed:</strong> {{ doctor.states_licensed }}</p>
            <p><strong>States Willing to Work:</strong> {{ doctor.states_willing_to_work }}</p>
            <p><strong>Salary Expectations:</strong> ${{ doctor.salary_expectations }}</p>
        </div>

        <div class="card shadow p-4 mb-4">
            <h5 class="card-title text-primary">Malpractice Cases</h5>
            {% if malpractice_cases %}
                {% for case in malpractice_cases %}
                    <p><strong>Incident Year:</strong> {{ case.incident_year }}</p>
                    <p><strong>Outcome:</strong> {{ case.outcome }}</p>
                    <p><strong>Payout Amount:</strong> ${{ case.payout_amount }}</p>
                    <hr>
                {% endfor %}
            {% else %}
                <p>No malpractice cases reported.</p>
            {% endif %}
        </div>

        <a href="{{ url_for('edit_doctor', doctor_id=doctor.id) }}" class="btn btn-warning">Edit Profile</a>
        <a href="{{ url_for('send_job_to_doctor', doctor_id=doctor.id) }}" class="btn btn-info">Send Job Posting</a>
        <a href="{{ url_for('doctors') }}" class="btn btn-secondary">Back to Doctors List</a>
    {% endblock %}''',

    'register_client.html': '''
        {% extends "base.html" %}
        {% block content %}
            <h2>Create Client Account</h2>
            <form method="post">
                {{ form.hidden_tag() }}
                <div class="mb-3">
                    {{ form.username.label }} {{ form.username(class="form-control") }}
                </div>
                <div class="mb-3">
                    {{ form.email.label }} {{ form.email(class="form-control") }}
                </div>
                <div class="mb-3">
                    {{ form.password.label }} {{ form.password(class="form-control") }}
                </div>
                {{ form.submit(class="btn btn-primary") }}
            </form>
        {% endblock %}''',

    'calls.html': '''{% extends "base.html" %}
        {% block content %}
            <h2>Scheduled Calls with Doctors</h2>

            <div id='calendar'></div>

            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    var calendarEl = document.getElementById('calendar');

                    var calendar = new FullCalendar.Calendar(calendarEl, {
                        initialView: 'dayGridMonth',
                        headerToolbar: {
                            left: 'prev,next today',
                            center: 'title',
                            right: 'dayGridMonth,timeGridWeek,timeGridDay'
                        },
                        height: 650,
                        events: {{ events | tojson }},
                        
                        // Add this block to handle event clicks:
                        eventClick: function(info) {
                            window.location.href = "/edit_call/" + info.event.id;
                        }
                    });

                    calendar.render();
                });
            </script>
        {% endblock %}''',

    'doctor_dashboard.html':'''{% extends "base.html" %}
        {% block content %}
        <h2>Welcome Dr. {{ doctor.first_name }} {{ doctor.last_name }}</h2>

        <div class="mb-3">
            <a class="btn btn-info" href="{{ url_for('doctor_edit_profile') }}">Edit Profile</a>
            <a class="btn btn-secondary" href="{{ url_for('doctor_jobs') }}">Jobs</a>
            <a class="btn btn-success" href="{{ url_for('doctor_inbox') }}">Inbox</a>
            <a class="btn btn-danger" href="{{ url_for('logout') }}">Logout</a>
        </div>

        <h4>Pending Invites</h4>
        {% for call in pending_invites %}
        <div class="alert alert-info">
            Invite from {{ call.scheduled_by.username }} on {{ call.datetime.strftime('%Y-%m-%d %H:%M') }} for "{{ call.reason }}"
            <br>
            <strong>Job:</strong> 
            <a href="{{ url_for('doctor_jobs') }}#job-{{ call.job.id }}">
                {{ call.job.title }}
            </a>
            <form method="post" action="{{ url_for('handle_invite', call_id=call.id) }}">
                <button name="action" value="accept" class="btn btn-success btn-sm">Accept</button>
                <button name="action" value="decline" class="btn btn-danger btn-sm">Decline</button>
            </form>
        </div>
        {% else %}
        <p>No pending invites.</p>
        {% endfor %}

        <div id="calendar"></div>

        <script>
        document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                height: 650,
                events: {{ events | tojson }},
                eventDidMount: function(info) {
                    // Tooltip showing event status clearly
                    let tooltip = new bootstrap.Tooltip(info.el, {
                        title: info.event.extendedProps.status,
                        placement: 'top',
                        trigger: 'hover',
                        container: 'body'
                    });

                    // Apply strikethrough for canceled meetings
                    if (info.event.extendedProps.status === 'Canceled') {
                        info.el.style.textDecoration = 'line-through';
                    }
                },
                eventClick: function(info) {
                    window.location.href = "/doctor/call/" + info.event.id;
                }
            });
            calendar.render();
        });
        </script>

        <!-- Include Bootstrap JS for Tooltips (ensure not duplicated) -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

        {% endblock %}''',


    'edit_job.html': '''{% extends "base.html" %}
    {% block content %}
        <h2>Edit Job: {{ job.title }}</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            <div class="mb-3">
                {{ form.title.label }} {{ form.title(class="form-control") }}
            </div>
            <div class="mb-3">
                {{ form.location.label }} {{ form.location(class="form-control") }}
            </div>
            <div class="mb-3">
                {{ form.salary.label }} {{ form.salary(class="form-control") }}
            </div>
            <div class="mb-3">
                {{ form.description.label }} {{ form.description(class="form-control") }}
            </div>
            {{ form.submit(class="btn btn-success") }}
        </form>
    {% endblock %}''',

    'doctor_edit_profile.html': '''{% extends "base.html" %}
    {% block content %}
        <h2>Edit My Profile</h2>
        <form method="post">
            {{ form.hidden_tag() }}

            <div class="mb-3">{{ form.position.label }} {{ form.position(class="form-select") }}</div>
            <div class="mb-3">{{ form.specialty.label }} {{ form.specialty(class="form-control") }}</div>
            <div class="mb-3">{{ form.subspecialty.label }} {{ form.subspecialty(class="form-control") }}</div>
            <div class="mb-3">{{ form.first_name.label }} {{ form.first_name(class="form-control") }}</div>
            <div class="mb-3">{{ form.last_name.label }} {{ form.last_name(class="form-control") }}</div>
            <div class="mb-3">{{ form.email.label }} {{ form.email(class="form-control") }}</div>
            <div class="mb-3">{{ form.phone.label }} {{ form.phone(class="form-control") }}</div>
            <div class="mb-3">{{ form.alt_phone.label }} {{ form.alt_phone(class="form-control") }}</div>
            <div class="mb-3">{{ form.city_of_residence.label }} {{ form.city_of_residence(class="form-control") }}</div>

            <h4>MD/DO Information</h4>
            <div class="mb-3">{{ form.medical_school.label }} {{ form.medical_school(class="form-control") }}</div>
            <div class="mb-3">{{ form.med_grad_month_year.label }} {{ form.med_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.residency.label }} {{ form.residency(class="form-control") }}</div>
            <div class="mb-3">{{ form.residency_grad_month_year.label }} {{ form.residency_grad_month_year(class="form-control") }}</div>

            <h4>Fellowships</h4>
            {% for fellowship_field in form.fellowship %}
                <div class="mb-3">{{ fellowship_field.label }} {{ fellowship_field(class="form-control") }}</div>
            {% endfor %}
            {% for fellowship_date_field in form.fellowship_grad_month_year %}
                <div class="mb-3">{{ fellowship_date_field.label }} {{ fellowship_date_field(class="form-control") }}</div>
            {% endfor %}

            <h4>NP/PA Information</h4>
            <div class="mb-3">{{ form.bachelors.label }} {{ form.bachelors(class="form-control") }}</div>
            <div class="mb-3">{{ form.bachelors_grad_month_year.label }} {{ form.bachelors_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.msn.label }} {{ form.msn(class="form-control") }}</div>
            <div class="mb-3">{{ form.msn_grad_month_year.label }} {{ form.msn_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.dnp.label }} {{ form.dnp(class="form-control") }}</div>
            <div class="mb-3">{{ form.dnp_grad_month_year.label }} {{ form.dnp_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.additional_training.label }} {{ form.additional_training(class="form-control") }}</div>
            <div class="form-check mb-3">{{ form.sponsorship_needed(class="form-check-input") }} {{ form.sponsorship_needed.label(class="form-check-label") }}</div>

            <h4>Certification & More</h4>
            <div class="mb-3">{{ form.certification.label }} {{ form.certification(class="form-select") }}</div>
            <div class="mb-3">{{ form.emr.label }} {{ form.emr(class="form-control") }}</div>
            <div class="mb-3">{{ form.languages.label }} {{ form.languages(class="form-control") }}</div>

            <h4>States Licensed</h4>
            {% for state in form.states_licensed %}
                <div class="form-check">{{ state }} {{ state.label }}</div>
            {% endfor %}

            <h4>States Willing to Work</h4>
            {% for state in form.states_willing_to_work %}
                <div class="form-check">{{ state }} {{ state.label }}</div>
            {% endfor %}

            <h4>Malpractice Cases</h4>
            {% for case in form.malpractice_cases %}
                <div class="border p-3 mb-3">
                    {{ case.incident_year.label }} {{ case.incident_year(class="form-control") }}
                    {{ case.outcome.label }} {{ case.outcome(class="form-select") }}
                    {{ case.payout_amount.label }} {{ case.payout_amount(class="form-control") }}
                </div>
            {% endfor %}

            <div class="mb-3">{{ form.salary_expectations.label }} {{ form.salary_expectations(class="form-control") }}</div>

            {{ form.submit(class="btn btn-success") }}
        </form>
    {% endblock %}''',

    'doctor_jobs.html': '''{% extends "base.html" %}
        {% block content %}
        <h2>Available Jobs</h2>
        <div class="list-group">
            {% for job in jobs %}
                <a href="{{ url_for('view_job', job_id=job.id) }}" class="list-group-item list-group-item-action" id="job-{{ job.id }}">
                    <h4>{{ job.title }}</h4>
                    <p>{{ job.description }}</p>
                    <p><strong>Location:</strong> {{ job.location }}</p>
                    <p><strong>Salary:</strong> {{ job.salary }}</p>
                </a>
            {% endfor %}
        </div>
        {% endblock %}''',

    'view_job.html': '''
    {% extends "base.html" %}
    {% block content %}
    <div class="card">
    <div class="card-body">
        <h3>{{ job.title }}</h3>
        <p><strong>Location:</strong> {{ job.location }}</p>
        <p><strong>Salary:</strong> {{ job.salary }}</p>
        <p>{{ job.description }}</p>

        <form method="post">
        <button class="btn btn-primary">Express Interest</button>
        </form>

        <a href="{{ url_for('doctor_jobs') }}" class="btn btn-secondary mt-3">Back to Jobs</a>
    </div>
    </div>
    {% endblock %}''',

    'inbox.html': '''{% extends 'base.html' %}
            {% block content %}
                <h2>{{ title }}</h2>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>From</th>
                            <th>Message</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for msg in messages %}
                        <tr>
                            <td>{{ msg.sender.username }}</td>
                            <td>
                                {{ msg.content }}
                                {% if msg.message_type == 'interest' %}
                                    <a href="{{ url_for('send_invite', doctor_id=msg.doctor_id, job_id=msg.job_id) }}" class="btn btn-primary btn-sm">Send Call Invite</a>
                                {% endif %}
                            </td>
                            <td>{{ msg.timestamp.strftime('%Y-%m-%d %H:%M') }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% endblock %}''',

    'doctor_call_details.html': '''
        {% extends "base.html" %}
        {% block content %}
        <h2>Scheduled Call Details</h2>

        <p><strong>With:</strong> {{ call.scheduled_by.username }} ({{ call.scheduled_by.role }})</p>
        <p><strong>Date & Time:</strong> {{ call.datetime }}</p>
        <p><strong>Reason:</strong> {{ call.reason }}</p>
        <p><strong>Status:</strong> {% if call.canceled %}Canceled{% elif call.reschedule_requested %}Reschedule Requested{% else %}Scheduled{% endif %}</p>

        {% if not call.canceled %}
        <form method="post">
            <button name="action" value="cancel" class="btn btn-danger">Cancel Meeting</button>
        </form>

        <h3 class="mt-4">Request Reschedule</h3>
        <form method="post">
            <div class="mb-3">
                <label>New Date & Time:</label>
                <input type="datetime-local" name="reschedule_datetime" class="form-control" required>
            </div>
            <div class="mb-3">
                <label>Reason for Reschedule:</label>
                <textarea name="reschedule_note" class="form-control"></textarea>
            </div>
            <button name="action" value="reschedule" class="btn btn-warning">Request Reschedule</button>
        </form>
        {% endif %}
        {% endblock %}''',

    'handle_reschedule.html': '''
        {% extends "base.html" %}
        {% block content %}
        <h2>Handle Reschedule Request</h2>

        <p><strong>Doctor:</strong> {{ call.doctor.first_name }} {{ call.doctor.last_name }}</p>
        <p><strong>Current Date & Time:</strong> {{ call.datetime }}</p>
        <p><strong>Requested Date & Time:</strong> {{ call.reschedule_datetime }}</p>
        <p><strong>Reason for Reschedule:</strong> {{ call.reschedule_note }}</p>

        <form method="post">
            <button name="action" value="accept" class="btn btn-success">Accept Request</button>
            <button name="action" value="reject" class="btn btn-danger">Reject Request</button>
        </form>
        {% endblock %}''',

    'doctors.html': '''{% extends "base.html" %}{% block content %}
        <h2>Doctors in System</h2>
        <table class="table table-striped">
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Specialty</th>
                <th>States Licensed</th>
                <th>States Willing to Work</th>
                <th>Salary Expectations</th>
                <th>Edit</th>
            </tr>
            {% for doctor in doctors %}
            <tr>
                <td><a href="{{ url_for('doctor_profile', doctor_id=doctor.id) }}">{{ doctor.first_name }} {{ doctor.last_name }}</a></td>
                <td>{{ doctor.email }}</td>
                <td>{{ doctor.phone }}</td>
                <td>{{ doctor.specialty }}</td>
                <td>{{ doctor.states_licensed.replace(",", ", ") if doctor.states_licensed else '' }}</td>
                <td>{{ doctor.states_willing_to_work.replace(",", ", ") if doctor.states_willing_to_work else '' }}</td>
                <td>${{ doctor.salary_expectations }}</td>
                <td>
                    <a href="{{ url_for('edit_doctor', doctor_id=doctor.id) }}" class="btn btn-warning btn-sm">Edit</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    {% endblock %}''',

    'edit_call.html': '''{% extends "base.html" %}
    {% block content %}
        <h2>Edit Scheduled Call</h2>
        <form method="post">
            {{ form.hidden_tag() }}

            <div class="mb-3">
                {{ form.doctor_id.label }}
                {{ form.doctor_id(class="form-select") }}
            </div>

            <div class="mb-3">
                {{ form.datetime.label }}
                {{ form.datetime(class="form-control", id="datetime") }}
            </div>

            <div class="mb-3">
                {{ form.reason.label }}
                {{ form.reason(class="form-control") }}
            </div>

            {{ form.submit(class="btn btn-success") }}
        </form>

        <!-- Include Select2 CSS and JS -->
        <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>

        <script>
            $(document).ready(function() {
                $('.form-select').select2({
                    placeholder: "Select Doctor (Name | Email | Specialty)",
                    allowClear: true,
                    width: '100%'
                });
            });
            flatpickr("#datetime", {enableTime: true, dateFormat: "Y-m-d\\TH:i"});
        </script>
    {% endblock %}''',

    'send_job.html': '''{% extends 'base.html' %}
    {% block content %}
        <h2>Send Job to {{ doctor.first_name }} {{ doctor.last_name }}</h2>
        <form method="post">
            <div class="mb-3">
                <label>Select Job:</label>
                <select name="job_id" class="form-select">
                    {% for job in jobs %}
                        <option value="{{ job.id }}">{{ job.title }} ({{ job.location }})</option>
                    {% endfor %}
                </select>
            </div>
            <button class="btn btn-success">Send Job</button>
        </form>
        {% endblock %}''',

    'edit_doctor.html': '''{% extends "base.html" %}{% block content %}
        <h2>Edit Doctor: {{ doctor.first_name }} {{ doctor.last_name }}</h2>
        <form method="post">
            {{ form.hidden_tag() }}

            <div class="mb-3">{{ form.position.label }} {{ form.position(class="form-select") }}</div>
            <div class="mb-3">{{ form.specialty.label }} {{ form.specialty(class="form-control") }}</div>
            <div class="mb-3">{{ form.subspecialty.label }} {{ form.subspecialty(class="form-control") }}</div>
            <div class="mb-3">{{ form.first_name.label }} {{ form.first_name(class="form-control") }}</div>
            <div class="mb-3">{{ form.last_name.label }} {{ form.last_name(class="form-control") }}</div>
            <div class="mb-3">{{ form.email.label }} {{ form.email(class="form-control") }}</div>
            <div class="mb-3">{{ form.phone.label }} {{ form.phone(class="form-control") }}</div>
            <div class="mb-3">{{ form.alt_phone.label }} {{ form.alt_phone(class="form-control") }}</div>
            <div class="mb-3">{{ form.city_of_residence.label }} {{ form.city_of_residence(class="form-control") }}</div>

            <h4>MD/DO Information</h4>
            <div class="mb-3">{{ form.medical_school.label }} {{ form.medical_school(class="form-control") }}</div>
            <div class="mb-3">{{ form.med_grad_month_year.label }} {{ form.med_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.residency.label }} {{ form.residency(class="form-control") }}</div>
            <div class="mb-3">{{ form.residency_grad_month_year.label }} {{ form.residency_grad_month_year(class="form-control") }}</div>

            <div id="fellowship_fields">
                {% for fellowship_field in form.fellowship %}
                    <div class="mb-3">{{ fellowship_field.label }} {{ fellowship_field(class="form-control") }}</div>
                {% endfor %}
                {% for fellowship_date_field in form.fellowship_grad_month_year %}
                    <div class="mb-3">{{ fellowship_date_field.label }} {{ fellowship_date_field(class="form-control") }}</div>
                {% endfor %}
            </div>

            <h4>NP/PA Information</h4>
            <div class="mb-3">{{ form.bachelors.label }} {{ form.bachelors(class="form-control") }}</div>
            <div class="mb-3">{{ form.bachelors_grad_month_year.label }} {{ form.bachelors_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.msn.label }} {{ form.msn(class="form-control") }}</div>
            <div class="mb-3">{{ form.msn_grad_month_year.label }} {{ form.msn_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.dnp.label }} {{ form.dnp(class="form-control") }}</div>
            <div class="mb-3">{{ form.dnp_grad_month_year.label }} {{ form.dnp_grad_month_year(class="form-control") }}</div>
            <div class="mb-3">{{ form.additional_training.label }} {{ form.additional_training(class="form-control") }}</div>
            <div class="form-check mb-3">{{ form.sponsorship_needed(class="form-check-input") }} {{ form.sponsorship_needed.label(class="form-check-label") }}</div>

            <h4>Malpractice Cases</h4>
            <div>
                {% for case in form.malpractice_cases %}
                    <div class="border p-3 mb-3 rounded">
                        <div class="mb-2">{{ case.incident_year.label }} {{ case.incident_year(class="form-control") }}</div>
                        <div class="mb-2">{{ case.outcome.label }} {{ case.outcome(class="form-select") }}</div>
                        <div class="mb-2">{{ case.payout_amount.label }} {{ case.payout_amount(class="form-control") }}</div>
                    </div>
                {% endfor %}
            </div>

            <div class="mb-3">{{ form.certification.label }} {{ form.certification(class="form-select") }}</div>
            <div class="mb-3">{{ form.emr.label }} {{ form.emr(class="form-control") }}</div>
            <div class="mb-3">{{ form.languages.label }} {{ form.languages(class="form-control") }}</div>

            <div class="mb-3">
                {{ form.states_licensed.label }}
                {% for state in form.states_licensed %}
                    <div class="form-check">{{ state }} {{ state.label }}</div>
                {% endfor %}
            </div>

            <div class="mb-3">
                {{ form.states_willing_to_work.label }}
                {% for state in form.states_willing_to_work %}
                    <div class="form-check">{{ state }} {{ state.label }}</div>
                {% endfor %}
            </div>

            <div class="mb-3">{{ form.salary_expectations.label }} {{ form.salary_expectations(class="form-control") }}</div>

            {{ form.submit(class="btn btn-success") }}
        </form>
        {% endblock %}'''
         })

# Routes
@app.route('/')
@login_required
def home():
    if current_user.role == 'admin':
        return render_template('index.html')
    elif current_user.role == 'client':
        return redirect(url_for('client_dashboard'))
    elif current_user.role == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    else:
        flash('Role not recognized.', 'danger')
        return redirect(url_for('login'))

@app.route('/send_job/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def send_job_to_doctor(doctor_id):
    if current_user.role not in ['admin', 'client']:
        flash('Unauthorized', 'danger')
        return redirect(url_for('home'))

    doctor = Doctor.query.get_or_404(doctor_id)
    doctor_user = User.query.get(doctor.user_id)

    # Ensure clients can only see their own jobs
    if current_user.role == 'admin':
        jobs = Job.query.all()
    else:  # client
        jobs = Job.query.filter_by(poster_id=current_user.id).all()

    if request.method == 'POST':
        job_id = request.form.get('job_id')
        job = Job.query.get_or_404(job_id)

        # Confirm clients only send their own job posts
        if current_user.role == 'client' and job.poster_id != current_user.id:
            flash('You can only send your own jobs.', 'danger')
            return redirect(url_for('home'))

        message = Message(
            sender_id=current_user.id,
            recipient_id=doctor_user.id,
            job_id=job.id,
            content=f"{current_user.username} has recommended the job: '{job.title}' for you."
        )

        db.session.add(message)
        db.session.commit()
        flash('Job sent to doctor!', 'success')
        return redirect(url_for('doctor_profile', doctor_id=doctor_id))

    return render_template('send_job.html', doctor=doctor, jobs=jobs)



@app.route('/doctor/inbox')
@login_required
def doctor_inbox():
    if current_user.role != 'doctor':
        flash('Unauthorized', 'danger')
        return redirect(url_for('home'))

    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    
    # Mark unread messages as read
    unread_messages = [msg for msg in messages if not msg.read]
    for msg in unread_messages:
        msg.read = True
    db.session.commit()

    return render_template('inbox.html', messages=messages, title="My Inbox")

@app.route('/admin/inbox')
@login_required
def admin_inbox():
    if current_user.role != 'admin':
        flash('Unauthorized', 'danger')
        return redirect(url_for('home'))

    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()

    unread_messages = [msg for msg in messages if not msg.read]
    for msg in unread_messages:
        msg.read = True
    db.session.commit()

    return render_template('inbox.html', messages=messages, title="Admin Inbox")

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        existing_doctor = Doctor.query.filter_by(email=form.email.data).first()

        if existing_doctor:
            flash('A doctor with this email already exists.', 'danger')
            return render_template('add_doctor.html', form=form)

        try:
            doctor = Doctor(
                position=form.position.data,
                specialty=form.specialty.data,
                subspecialty=form.subspecialty.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                alt_phone=form.alt_phone.data,
                city_of_residence=form.city_of_residence.data,
                medical_school=form.medical_school.data,
                med_grad_month_year=form.med_grad_month_year.data,
                residency=form.residency.data,
                residency_grad_month_year=form.residency_grad_month_year.data,
                fellowship=",".join(form.fellowship.data),
                fellowship_grad_month_year=",".join(form.fellowship_grad_month_year.data),
                bachelors=form.bachelors.data,
                bachelors_grad_month_year=form.bachelors_grad_month_year.data,
                msn=form.msn.data,
                msn_grad_month_year=form.msn_grad_month_year.data,
                dnp=form.dnp.data,
                dnp_grad_month_year=form.dnp_grad_month_year.data,
                additional_training=form.additional_training.data,
                sponsorship_needed=form.sponsorship_needed.data,
                malpractice_cases=json.dumps([
                    {
                        'incident_year': case.incident_year.data,
                        'outcome': case.outcome.data,
                        'payout_amount': case.payout_amount.data or 0
                    } for case in form.malpractice_cases if case.incident_year.data
                ]),
                certification=form.certification.data,
                emr=form.emr.data,
                languages=form.languages.data,
                states_licensed=",".join(form.states_licensed.data),
                states_willing_to_work=",".join(form.states_willing_to_work.data),
                salary_expectations=form.salary_expectations.data or 0.0
            )
            db.session.add(doctor)
            db.session.commit()
            flash('Doctor added successfully!', 'success')
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding doctor: {e}", 'danger')
            print(f"Error adding doctor: {e}")
    else:
        if request.method == 'POST':
            flash(f"Form errors: {form.errors}", 'danger')

    return render_template('add_doctor.html', form=form)


@app.route('/schedule_call', methods=['GET', 'POST'])
@login_required
def schedule_call():
    form = ScheduledCallForm()

    form.doctor_id.choices = [
        (doc.id, f"{doc.first_name} {doc.last_name} | {doc.email} | {doc.specialty}") 
        for doc in Doctor.query.order_by(Doctor.last_name).all()
    ]

    if form.validate_on_submit():
        dt = form.datetime.data  # <-- FIX HERE

        invite_status = "Pending" if request.form.get('send_invite') == 'yes' else "Accepted"

        call = ScheduledCall(
            doctor_id=form.doctor_id.data,
            scheduled_by_id=current_user.id,
            job_id=None,
            datetime=dt,
            reason=form.reason.data,
            invite_status=invite_status
        )
        db.session.add(call)
        db.session.commit()

        if invite_status == "Pending":
            doctor = Doctor.query.get(form.doctor_id.data)
            doctor_user = User.query.get(doctor.user_id)
            if doctor_user:
                message = Message(
                    sender_id=current_user.id,
                    recipient_id=doctor_user.id,
                    content=(
                        f"You have a new call invite scheduled on {dt.strftime('%Y-%m-%d %H:%M')} "
                        f"for reason: {form.reason.data}. Please accept or decline on your dashboard."
                    )
                )
                db.session.add(message)
                db.session.commit()
                flash('Invite sent to doctor successfully!', 'success')
        else:
            flash('Call scheduled successfully!', 'success')

        return redirect(url_for('home'))

    return render_template('schedule_call.html', form=form)






@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('home'))

    scheduled_calls = ScheduledCall.query.order_by(ScheduledCall.datetime).all()

    events = [
        {
            'id': call.id,
            'title': call.doctor.first_name + " " + call.doctor.last_name + " - " + (call.reason or "No Reason"),
            'start': call.datetime.strftime('%Y-%m-%dT%H:%M:%S'),
        } for call in scheduled_calls
    ]

    return render_template('index.html', events=events)


@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/edit_call/<int:call_id>', methods=['GET', 'POST'])
@login_required
def edit_call(call_id):
    scheduled_call = ScheduledCall.query.get_or_404(call_id)
    form = ScheduledCallForm(obj=scheduled_call)

    form.doctor_id.choices = [
        (doc.id, f"{doc.first_name} {doc.last_name} | {doc.email} | {doc.specialty}") 
        for doc in Doctor.query.order_by(Doctor.last_name).all()
    ]

    if form.validate_on_submit():
        # Check if datetime or doctor has changed
        original_datetime = scheduled_call.datetime
        original_doctor_id = scheduled_call.doctor_id

        scheduled_call.doctor_id = form.doctor_id.data
        scheduled_call.datetime = form.datetime.data if isinstance(form.datetime.data, datetime) else datetime.strptime(form.datetime.data, '%Y-%m-%dT%H:%M')
        scheduled_call.reason = form.reason.data
        
        db.session.commit()

        # Send notification to doctor's inbox if rescheduled
        if (scheduled_call.datetime != original_datetime or 
            scheduled_call.doctor_id != original_doctor_id):

            doctor_user = User.query.filter_by(doctor_id=scheduled_call.doctor_id).first()
            if doctor_user:
                message = Message(
                    sender_id=current_user.id,
                    recipient_id=doctor_user.id,
                    content=(
                        f"The scheduled meeting has been rescheduled to "
                        f"{scheduled_call.datetime.strftime('%Y-%m-%d %H:%M')} "
                        f"by {current_user.username}."
                    )
                )
                db.session.add(message)
                db.session.commit()

        flash('Scheduled call updated successfully!', 'success')
        return redirect(url_for('calls'))

    form.doctor_id.data = scheduled_call.doctor_id
    form.datetime.data = scheduled_call.datetime 
    form.reason.data = scheduled_call.reason

    return render_template('edit_call.html', form=form, call=scheduled_call)





#@app.route('/static/<path:filename>')
#def custom_static(filename):
    #full_path = r'C:\Users\Tubam\OneDrive\Desktop\static'
    #print(f"Serving file: {filename} from path: {full_path}")
    #return send_from_directory(full_path, filename)

@app.route('/calls')
def calls():
    scheduled_calls = ScheduledCall.query.order_by(ScheduledCall.datetime).all()
    events = [
    {
        'id': call.id,
        'title': call.doctor.first_name + " " + call.doctor.last_name + " - " + (call.reason or "No Reason"),
        'start': call.datetime.strftime('%Y-%m-%dT%H:%M:%S'),
    } for call in scheduled_calls
    ]
    return render_template('calls.html', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            
            # Redirect users immediately based on their role
            if user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user.role == 'client':
                return redirect(url_for('client_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('home'))
            else:
                flash('Role not recognized.', 'danger')
                return redirect(url_for('login'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)


@app.route('/register_doctor', methods=['GET', 'POST'])
@login_required
def register_doctor():
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('home'))

    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()

        if existing_user:
            flash('Username or email already exists for user login.', 'danger')
            return redirect(url_for('register_doctor'))

        # Check if doctor profile already exists with the email provided
        existing_doctor = Doctor.query.filter_by(email=form.email.data).first()

        if existing_doctor:
            # Create user linked to existing doctor profile
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                role='doctor'
            )
            db.session.add(new_user)
            db.session.commit()

            # Associate the existing doctor with the new user's ID
            existing_doctor.user_id = new_user.id
            db.session.commit()

            flash('Doctor login linked to existing profile!', 'success')
            return redirect(url_for('home'))

        # First create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role='doctor'
        )
        db.session.add(new_user)
        db.session.commit()

        # Then create new doctor profile associated to the new user
        new_doctor = Doctor(
            first_name='',
            last_name='',
            email=form.email.data,
            position='',
            specialty='',
            joined=datetime.utcnow(),
            user_id=new_user.id  # <-- Associate new doctor with new user
        )
        db.session.add(new_doctor)
        db.session.commit()

        # Finally, link newly created doctor profile back to user
        new_user.doctor_id = new_doctor.id
        db.session.commit()

        flash('New Doctor account created and linked!', 'success')
        return redirect(url_for('home'))

    return render_template('register_doctor.html', form=form)


@app.route('/scrape_jobs')
@login_required
def scrape_jobs():
    if current_user.role not in ['user', 'admin']:
        flash('Unauthorized access!', 'danger') 
        return redirect(url_for('home'))

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
    from bs4 import BeautifulSoup
    import time

    URL = 'https://www.doccafe.com/company/jobs'  

    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(URL)

    input("✅ Please log into Doc Cafe now. Once you've logged in, press Enter to continue scraping...")

    jobs_added = 0

    try:
        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "col-lg-8"))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_elements = soup.find_all('div', class_='col-lg-8 col-sm-11 col-xs-10 no-padding-left')

            for job in job_elements:
                link_tag = job.find('h4').find('a', href=True)
                job_url = link_tag['href']
                job_title_tag = link_tag.find('span')
                job_title = job_title_tag.get_text(strip=True) if job_title_tag else 'N/A'

                # Open job detail page
                driver.execute_script("window.open(arguments[0]);", job_url)
                driver.switch_to.window(driver.window_handles[1])

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "job-summary"))
                )

                job_soup = BeautifulSoup(driver.page_source, 'html.parser')

                pay = job_soup.find('span', class_='job-salary-amount').get_text(strip=True) if job_soup.find('span', class_='job-salary-amount') else 'N/A'
                location = job_soup.find('span', class_='job-summary-location').get_text(strip=True) if job_soup.find('span', class_='job-summary-location') else 'N/A'
                description_tag = job_soup.find('div', class_='job-summary-box_field_6')
                description = description_tag.get_text(strip=True) if description_tag else 'N/A'

                # Save to database directly
                new_job = Job(
                    title=job_title,
                    location=location,
                    salary=pay,
                    description=description,
                    poster_id=current_user.id
                )
                db.session.add(new_job)
                db.session.commit()
                jobs_added += 1

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            try:
                next_button = driver.find_element(By.XPATH, '//a[@rel="next"]')
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
            except (NoSuchElementException, ElementClickInterceptedException):
                flash("No more pages or unable to click next button.", "info")
                break

    except TimeoutException:
        flash("Timed out waiting for page to load.", "danger")
    finally:
        driver.quit()

    flash(f"{jobs_added} job postings successfully added!", "success")
    return redirect(url_for('doctor_jobs'))


@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role not in ['client', 'admin']:
        flash('Only clients and admins can post jobs!', 'danger')
        return redirect(url_for('home'))

    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            location=form.location.data,
            salary=form.salary.data,
            description=form.description.data,
            poster_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')

        if current_user.role == 'admin':
            return redirect(url_for('home'))
        elif current_user.role == 'client':
            return redirect(url_for('client_dashboard'))

    return render_template('post_job.html', form=form)




@app.route('/doctor/jobs')
@login_required
def doctor_jobs():
    if current_user.role != 'doctor':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('doctor_dashboard'))

    jobs = Job.query.all()
    return render_template('doctor_jobs.html', jobs=jobs)


@app.route('/doctor/job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def view_job(job_id):
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        # Express interest explicitly
        recipient_user = job.poster
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_user.id,
            job_id=job.id,
            doctor_id=current_user.doctor.id,
            content=f"Dr. {current_user.doctor.first_name} {current_user.doctor.last_name} expressed interest in your job '{job.title}'.",
            message_type='interest'
        )
        db.session.add(message)
        db.session.commit()

        flash('Your interest has been sent to the client.', 'success')
        return redirect(url_for('doctor_jobs'))

    return render_template('view_job.html', job=job)



@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    doctor = current_user.doctor

    scheduled_calls = ScheduledCall.query.filter_by(doctor_id=doctor.id).all()
    pending_invites = ScheduledCall.query.filter_by(doctor_id=doctor.id, invite_status='Pending').all()

    events = []
    for call in scheduled_calls:
        # Determine the color and status clearly
        if call.canceled:
            color, status = '#ff4d4d', 'Canceled'
        elif call.reschedule_requested:
            color, status = '#3788d8', 'Reschedule Requested'
        elif call.invite_status.lower() == 'pending':
            color, status = '#ffc107', 'Pending Invite'
        elif call.invite_status.lower() == 'accepted':
            color, status = '#28a745', 'Accepted'
        else:
            color, status = '#6c757d', 'Scheduled'

        events.append({
            'id': call.id,
            'title': f"Call with {call.scheduled_by.username}",
            'start': call.datetime.isoformat(),
            'color': color,
            'status': status
        })

    return render_template('doctor_dashboard.html', doctor=doctor, events=events, pending_invites=pending_invites)


@app.route('/handle_invite/<int:call_id>', methods=['POST'])
@login_required
def handle_invite(call_id):
    scheduled_call = ScheduledCall.query.get_or_404(call_id)

    if current_user.doctor.id != scheduled_call.doctor_id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('doctor_dashboard'))

    action = request.form.get('action')
    if action == 'accept':
        scheduled_call.invite_status = 'accepted'
        flash('Invite accepted.', 'success')

        # Notify client of acceptance
        content = f"Dr. {current_user.doctor.first_name} {current_user.doctor.last_name} accepted your call invite."
    elif action == 'decline':
        scheduled_call.invite_status = 'declined'
        flash('Invite declined.', 'info')

        # Notify client of decline
        content = f"Dr. {current_user.doctor.first_name} {current_user.doctor.last_name} declined your call invite."
    else:
        flash('Invalid action.', 'danger')
        return redirect(url_for('doctor_dashboard'))

    # Send notification message back to client
    notification = Message(
        sender_id=current_user.id,
        recipient_id=scheduled_call.scheduled_by_id,
        doctor_id=current_user.doctor.id,
        content=content,
        message_type='invite_response'
    )

    db.session.add(notification)
    db.session.commit()

    return redirect(url_for('doctor_dashboard'))


@app.route('/doctor/handle_invite/<int:call_id>', methods=['POST'])
@login_required
def doctor_handle_invite(call_id):
    scheduled_call = ScheduledCall.query.get_or_404(call_id)

    action = request.form.get('action')

    if action == 'accept':
        scheduled_call.invite_status = "Accepted"
        flash('Invite accepted!', 'success')

        notification = Message(
            sender_id=current_user.id,
            recipient_id=scheduled_call.scheduled_by_id,
            content=f"Dr. {current_user.doctor.first_name} {current_user.doctor.last_name} accepted your meeting invite scheduled on {scheduled_call.datetime.strftime('%Y-%m-%d %H:%M')}."
        )

    elif action == 'decline':
        scheduled_call.invite_status = "Declined"
        flash('Invite declined!', 'danger')

        notification = Message(
            sender_id=current_user.id,
            recipient_id=scheduled_call.scheduled_by_id,
            content=f"Dr. {current_user.doctor.first_name} {current_user.doctor.last_name} declined your meeting invite scheduled on {scheduled_call.datetime.strftime('%Y-%m-%d %H:%M')}."
        )

    db.session.add(notification)
    db.session.commit()

    return redirect(url_for('doctor_dashboard'))


@app.route('/doctor/handle_reschedule/<int:call_id>', methods=['GET', 'POST'])
@login_required
def doctor_handle_reschedule(call_id):
    scheduled_call = ScheduledCall.query.get_or_404(call_id)

    if current_user.id != scheduled_call.doctor.user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('doctor_dashboard'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'accept':
            scheduled_call.datetime = scheduled_call.reschedule_datetime
            scheduled_call.reschedule_requested = False
            scheduled_call.reschedule_note = None
            scheduled_call.reschedule_datetime = None
            db.session.commit()
            flash('Reschedule accepted.', 'success')

        elif action == 'reject':
            scheduled_call.reschedule_requested = False
            scheduled_call.reschedule_note = None
            scheduled_call.reschedule_datetime = None
            db.session.commit()
            flash('Reschedule request rejected.', 'warning')

        return redirect(url_for('doctor_dashboard'))

    return render_template('handle_reschedule.html', call=scheduled_call)

@app.route('/register_client', methods=['GET', 'POST'])
@login_required
def register_client():
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('home'))

    form = ClientRegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()

        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register_client'))

        new_client = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role='client'
        )
        db.session.add(new_client)
        db.session.commit()

        flash('New client account created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('register_client.html', form=form)

@app.route('/doctor/job/<int:job_id>/express_interest', methods=['POST'])
@login_required
def express_interest(job_id):
    job = Job.query.get_or_404(job_id)

    if current_user.role != 'doctor':
        flash('Unauthorized', 'danger')
        return redirect(url_for('doctor_jobs'))

    recipient_user = job.poster

    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient_user.id,
        job_id=job.id,
        doctor_id=current_user.doctor.id,
        content=f"{current_user.doctor.first_name} {current_user.doctor.last_name} expressed interest in your job: '{job.title}'.",
        message_type='interest'  # <-- clearly marked interest message
    )

    db.session.add(message)
    db.session.commit()

    flash('Interest sent to client!', 'success')
    return redirect(url_for('doctor_jobs'))

@app.route('/send_invite/<int:doctor_id>/<int:job_id>', methods=['GET', 'POST'])
@login_required
def send_invite(doctor_id, job_id):
    if current_user.role not in ['client', 'admin']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    doctor = Doctor.query.get_or_404(doctor_id)
    doctor_user = User.query.filter_by(id=doctor.user_id).first_or_404()
    job = Job.query.get_or_404(job_id)

    form = ScheduledCallForm()
    form.doctor_id.choices = [(doctor.id, f"{doctor.first_name} {doctor.last_name} | {doctor.email}")]

    if form.validate_on_submit():
        scheduled_call = ScheduledCall(
            doctor_id=doctor.id,
            scheduled_by_id=current_user.id,
            job_id=job.id,
            datetime=form.datetime.data,
            reason=form.reason.data,
            invite_status='pending'
        )

        db.session.add(scheduled_call)
        db.session.commit()

        # Send invite message to doctor
        message = Message(
            sender_id=current_user.id,
            recipient_id=doctor_user.id,
            job_id=job_id,
            doctor_id=doctor.id,
            content=f"You have a call invite scheduled by {current_user.username} on {form.datetime.data}.",
            message_type='invite'
        )
        db.session.add(message)
        db.session.commit()

        flash('Invite sent to doctor!', 'success')

        # Redirect to appropriate dashboard
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('client_dashboard'))

    return render_template('schedule_call.html', form=form, job=job, doctor=doctor)


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)

    if current_user.role != 'client' or job.poster_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('home'))

    form = JobForm(obj=job)

    if form.validate_on_submit():
        job.title = form.title.data
        job.location = form.location.data
        job.salary = form.salary.data
        job.description = form.description.data

        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('client_my_jobs'))

    return render_template('edit_job.html', form=form, job=job)


@app.route('/doctor/edit_profile', methods=['GET', 'POST'])
@login_required
def doctor_edit_profile():
    if current_user.role != 'doctor':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('home'))

    doctor = current_user.doctor

    if not doctor:
        flash("Doctor profile not found. Please contact the administrator.", "danger")
        return redirect(url_for('doctor_dashboard'))

    form = DoctorForm()

    if form.validate_on_submit():
        # Update doctor fields from form explicitly
        doctor.position = form.position.data
        doctor.specialty = form.specialty.data
        doctor.subspecialty = form.subspecialty.data
        doctor.first_name = form.first_name.data
        doctor.last_name = form.last_name.data
        doctor.email = form.email.data
        doctor.phone = form.phone.data
        doctor.alt_phone = form.alt_phone.data
        doctor.city_of_residence = form.city_of_residence.data
        doctor.medical_school = form.medical_school.data
        doctor.med_grad_month_year = form.med_grad_month_year.data
        doctor.residency = form.residency.data
        doctor.residency_grad_month_year = form.residency_grad_month_year.data
        doctor.fellowship = ",".join(form.fellowship.data)
        doctor.fellowship_grad_month_year = ",".join(form.fellowship_grad_month_year.data)
        doctor.bachelors = form.bachelors.data
        doctor.bachelors_grad_month_year = form.bachelors_grad_month_year.data
        doctor.msn = form.msn.data
        doctor.msn_grad_month_year = form.msn_grad_month_year.data
        doctor.dnp = form.dnp.data
        doctor.dnp_grad_month_year = form.dnp_grad_month_year.data
        doctor.additional_training = form.additional_training.data
        doctor.sponsorship_needed = form.sponsorship_needed.data
        doctor.malpractice_cases = json.dumps([
            {
                'incident_year': case.incident_year.data,
                'outcome': case.outcome.data,
                'payout_amount': case.payout_amount.data
            } for case in form.malpractice_cases
        ])
        doctor.certification = form.certification.data
        doctor.emr = form.emr.data
        doctor.languages = form.languages.data
        doctor.states_licensed = ",".join(form.states_licensed.data)
        doctor.states_willing_to_work = ",".join(form.states_willing_to_work.data)
        doctor.salary_expectations = form.salary_expectations.data

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))

    elif request.method == 'GET':
        # Explicitly pre-fill simple fields
        form.position.data = doctor.position
        form.specialty.data = doctor.specialty
        form.subspecialty.data = doctor.subspecialty
        form.first_name.data = doctor.first_name
        form.last_name.data = doctor.last_name
        form.email.data = doctor.email
        form.phone.data = doctor.phone
        form.alt_phone.data = doctor.alt_phone
        form.city_of_residence.data = doctor.city_of_residence
        form.medical_school.data = doctor.medical_school
        form.med_grad_month_year.data = doctor.med_grad_month_year
        form.residency.data = doctor.residency
        form.residency_grad_month_year.data = doctor.residency_grad_month_year
        form.bachelors.data = doctor.bachelors
        form.bachelors_grad_month_year.data = doctor.bachelors_grad_month_year
        form.msn.data = doctor.msn
        form.msn_grad_month_year.data = doctor.msn_grad_month_year
        form.dnp.data = doctor.dnp
        form.dnp_grad_month_year.data = doctor.dnp_grad_month_year
        form.additional_training.data = doctor.additional_training
        form.sponsorship_needed.data = doctor.sponsorship_needed
        form.certification.data = doctor.certification
        form.emr.data = doctor.emr
        form.languages.data = doctor.languages
        form.salary_expectations.data = doctor.salary_expectations

        # Multi-select fields explicitly
        form.states_licensed.data = doctor.states_licensed.split(",") if doctor.states_licensed else []
        form.states_willing_to_work.data = doctor.states_willing_to_work.split(",") if doctor.states_willing_to_work else []

        # Malpractice cases (ensuring maximum entries limit)
        malpractice_cases = json.loads(doctor.malpractice_cases or '[]')
        form.malpractice_cases.entries.clear()
        for case in malpractice_cases[:form.malpractice_cases.max_entries]:
            form.malpractice_cases.append_entry({
                'incident_year': case.get('incident_year', ''),
                'outcome': case.get('outcome', ''),
                'payout_amount': case.get('payout_amount', 0)
            })
        while len(form.malpractice_cases.entries) < form.malpractice_cases.min_entries:
            form.malpractice_cases.append_entry()

        # Fellowships with a safe maximum (e.g., 10)
        MAX_FELLOWSHIPS = 10
        fellowships = doctor.fellowship.split(",") if doctor.fellowship else []
        fellowship_dates = doctor.fellowship_grad_month_year.split(",") if doctor.fellowship_grad_month_year else []

        form.fellowship.entries.clear()
        for fellowship in fellowships[:MAX_FELLOWSHIPS]:
            form.fellowship.append_entry(fellowship)
        while len(form.fellowship.entries) < form.fellowship.min_entries:
            form.fellowship.append_entry()

        form.fellowship_grad_month_year.entries.clear()
        for date in fellowship_dates[:MAX_FELLOWSHIPS]:
            form.fellowship_grad_month_year.append_entry(date)
        while len(form.fellowship_grad_month_year.entries) < form.fellowship_grad_month_year.min_entries:
            form.fellowship_grad_month_year.append_entry()

    return render_template('doctor_edit_profile.html', form=form, doctor=doctor)


    # Pre-fill form fields safely on GET
    if request.method == 'GET':
        form.states_licensed.data = doctor.states_licensed.split(",") if doctor.states_licensed else []
        form.states_willing_to_work.data = doctor.states_willing_to_work.split(",") if doctor.states_willing_to_work else []

        # Malpractice Cases handling with safety check
        malpractice_cases = json.loads(doctor.malpractice_cases or '[]')
        form.malpractice_cases.entries.clear()
        for case in malpractice_cases[:form.malpractice_cases.max_entries]:
            form.malpractice_cases.append_entry({
                'incident_year': case.get('incident_year', ''),
                'outcome': case.get('outcome', ''),
                'payout_amount': case.get('payout_amount', 0)
            })
        while len(form.malpractice_cases.entries) < form.malpractice_cases.min_entries:
            form.malpractice_cases.append_entry()

        # Fellowships with clear safety limit (10 entries for example)
        MAX_FELLOWSHIPS = 10
        fellowships = doctor.fellowship.split(",") if doctor.fellowship else []
        fellowship_dates = doctor.fellowship_grad_month_year.split(",") if doctor.fellowship_grad_month_year else []

        form.fellowship.entries.clear()
        for fellowship in fellowships[:MAX_FELLOWSHIPS]:
            form.fellowship.append_entry(fellowship)
        while len(form.fellowship.entries) < form.fellowship.min_entries:
            form.fellowship.append_entry()

        form.fellowship_grad_month_year.entries.clear()
        for date in fellowship_dates[:MAX_FELLOWSHIPS]:
            form.fellowship_grad_month_year.append_entry(date)
        while len(form.fellowship_grad_month_year.entries) < form.fellowship_grad_month_year.min_entries:
            form.fellowship_grad_month_year.append_entry()
    return render_template('doctor_edit_profile.html', form=form, doctor=doctor)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/client/inbox')
@login_required
def client_inbox():
    if current_user.role != 'client':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))

    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()

    unread_messages = [msg for msg in messages if not msg.read]
    for msg in unread_messages:
        msg.read = True
    db.session.commit()

    return render_template('inbox.html', messages=messages, title="Client Inbox")

@app.route('/register', methods=['GET', 'POST'])
@login_required  # Only logged-in users can create new accounts
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists.', 'danger')
        else:
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('New user registered successfully!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/test_db')
def test_db():
    try:
        db.session.execute("SELECT 1")
        return "Connection successful!"
    except Exception as e:
        return f"Connection failed: {e}"

@app.route('/client/dashboard')
@login_required
def client_dashboard():
    scheduled_calls = ScheduledCall.query.filter_by(scheduled_by_id=current_user.id).all()
    reschedule_requests = ScheduledCall.query.filter_by(
        scheduled_by_id=current_user.id, reschedule_requested=True
    ).all()

    events = []
    for call in scheduled_calls:
        if call.canceled:
            color, status = '#dc3545', 'Canceled'
        elif call.reschedule_requested:
            color, status = '#17a2b8', 'Reschedule Requested'
        elif call.invite_status == 'Pending':
            color, status = '#ffc107', 'Pending Invite'
        else:
            color, status = '#28a745', 'Accepted'

        events.append({
            'id': call.id,
            'title': f"Call with Dr. {call.doctor.first_name} {call.doctor.last_name}",
            'start': call.datetime.isoformat(),
            'color': color,
            'status': status,
        })

    return render_template(
        'client_dashboard.html',
        events=events,
        reschedule_requests=reschedule_requests
    )



@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('home'))
    elif current_user.role == 'client':
        return redirect(url_for('client_dashboard'))
    elif current_user.role == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    else:
        flash('Role not recognized.', 'danger')
        return redirect(url_for('login'))

@app.route('/doctor/call/<int:call_id>', methods=['GET', 'POST'])
@login_required
def doctor_call_details(call_id):
    scheduled_call = ScheduledCall.query.get_or_404(call_id)

    if current_user.role != 'doctor' or scheduled_call.doctor_id != current_user.doctor.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('doctor_dashboard'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'cancel':
            scheduled_call.canceled = True
            db.session.commit()
            flash('Meeting canceled.', 'success')
            return redirect(url_for('doctor_dashboard'))

        elif action == 'reschedule':
            new_datetime = request.form.get('reschedule_datetime')
            note = request.form.get('reschedule_note')

            scheduled_call.reschedule_requested = True
            scheduled_call.reschedule_note = note
            scheduled_call.reschedule_datetime = datetime.strptime(new_datetime, '%Y-%m-%dT%H:%M')
            db.session.commit()

            # Put the notification code HERE
            message = Message(
                sender_id=current_user.id,
                recipient_id=scheduled_call.scheduled_by_id,
                content=f"Reschedule requested for call on {scheduled_call.datetime.strftime('%Y-%m-%d %H:%M')} to {scheduled_call.reschedule_datetime.strftime('%Y-%m-%d %H:%M')}. Reason: {scheduled_call.reschedule_note}"
            )
            db.session.add(message)
            db.session.commit()

            flash('Reschedule requested sent.', 'success')
            return redirect(url_for('doctor_dashboard'))

    return render_template('doctor_call_details.html', call=scheduled_call)

@app.route('/client/my_jobs')
@login_required
def client_my_jobs():
    if current_user.role != 'client':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('home'))

    jobs = Job.query.filter_by(poster_id=current_user.id).all()
    return render_template('client_my_jobs.html', jobs=jobs)


@app.route('/doctor/<int:doctor_id>')
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    malpractice_cases = json.loads(doctor.malpractice_cases or '[]')
    return render_template('doctor_profile.html', doctor=doctor, malpractice_cases=malpractice_cases)

@app.route('/client/handle_reschedule/<int:call_id>', methods=['POST'])
@login_required
def client_handle_reschedule(call_id):
    scheduled_call = ScheduledCall.query.get_or_404(call_id)
    action = request.form.get('action')
    client_note = request.form.get('client_note', '')

    if action == 'accept':
        scheduled_call.datetime = scheduled_call.reschedule_datetime
        scheduled_call.reschedule_requested = False
        scheduled_call.reschedule_note = None
        scheduled_call.reschedule_datetime = None
        content = (f"Your reschedule request for "
                   f"{scheduled_call.datetime.strftime('%Y-%m-%d %H:%M')} has been accepted. {client_note}")
    elif action == 'decline':
        scheduled_call.reschedule_requested = False
        declined_datetime = scheduled_call.reschedule_datetime
        scheduled_call.reschedule_datetime = None
        scheduled_call.reschedule_note = None
        content = (f"Your reschedule request for "
                   f"{declined_datetime.strftime('%Y-%m-%d %H:%M')} has been declined. {client_note}")

    db.session.commit()

    message = Message(
        sender_id=current_user.id,
        recipient_id=scheduled_call.doctor.user_id,  # Corrected this line
        content=content,
        timestamp=datetime.utcnow()
    )

    db.session.add(message)
    db.session.commit()

    flash('Reschedule handled successfully.', 'success')
    return redirect(url_for('client_dashboard'))




@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            existing_doctor = Doctor.query.filter(
                Doctor.email == form.email.data, Doctor.id != doctor_id
            ).first()
            if existing_doctor:
                flash('Another doctor with this email already exists.', 'danger')
                return redirect(url_for('edit_doctor', doctor_id=doctor_id))

            # Populate simple fields explicitly
            doctor.position = form.position.data
            doctor.specialty = form.specialty.data
            doctor.subspecialty = form.subspecialty.data
            doctor.first_name = form.first_name.data
            doctor.last_name = form.last_name.data
            doctor.email = form.email.data
            doctor.phone = form.phone.data
            doctor.alt_phone = form.alt_phone.data
            doctor.city_of_residence = form.city_of_residence.data
            doctor.medical_school = form.medical_school.data
            doctor.med_grad_month_year = form.med_grad_month_year.data
            doctor.residency = form.residency.data
            doctor.residency_grad_month_year = form.residency_grad_month_year.data
            doctor.bachelors = form.bachelors.data
            doctor.bachelors_grad_month_year = form.bachelors_grad_month_year.data
            doctor.msn = form.msn.data
            doctor.msn_grad_month_year = form.msn_grad_month_year.data
            doctor.dnp = form.dnp.data
            doctor.dnp_grad_month_year = form.dnp_grad_month_year.data
            doctor.additional_training = form.additional_training.data
            doctor.sponsorship_needed = form.sponsorship_needed.data
            doctor.certification = form.certification.data
            doctor.emr = form.emr.data
            doctor.languages = form.languages.data
            doctor.salary_expectations = form.salary_expectations.data

            # Explicitly handle multi-select fields:
            doctor.states_licensed = ",".join(form.states_licensed.data)
            doctor.states_willing_to_work = ",".join(form.states_willing_to_work.data)

            # Explicitly handle Malpractice Cases JSON:
            doctor.malpractice_cases = json.dumps([
                {
                    'incident_year': case_form.incident_year.data,
                    'outcome': case_form.outcome.data,
                    'payout_amount': case_form.payout_amount.data
                } for case_form in form.malpractice_cases
            ])

            # Explicitly handle Fellowship fields:
            doctor.fellowship = ",".join(form.fellowship.data)
            doctor.fellowship_grad_month_year = ",".join(form.fellowship_grad_month_year.data)

            db.session.commit()
            flash('Doctor information updated successfully!', 'success')
            return redirect(url_for('doctor_profile', doctor_id=doctor.id))
        else:
            flash(f"Form errors: {form.errors}", 'danger')

    # Correct pre-fill for GET requests
    if request.method == 'GET':
        form = DoctorForm()

        # Populate simple fields manually
        form.position.data = doctor.position
        form.specialty.data = doctor.specialty
        form.subspecialty.data = doctor.subspecialty
        form.first_name.data = doctor.first_name
        form.last_name.data = doctor.last_name
        form.email.data = doctor.email
        form.phone.data = doctor.phone
        form.alt_phone.data = doctor.alt_phone
        form.city_of_residence.data = doctor.city_of_residence
        form.medical_school.data = doctor.medical_school
        form.med_grad_month_year.data = doctor.med_grad_month_year
        form.residency.data = doctor.residency
        form.residency_grad_month_year.data = doctor.residency_grad_month_year
        form.bachelors.data = doctor.bachelors
        form.bachelors_grad_month_year.data = doctor.bachelors_grad_month_year
        form.msn.data = doctor.msn
        form.msn_grad_month_year.data = doctor.msn_grad_month_year
        form.dnp.data = doctor.dnp
        form.dnp_grad_month_year.data = doctor.dnp_grad_month_year
        form.additional_training.data = doctor.additional_training
        form.sponsorship_needed.data = doctor.sponsorship_needed
        form.certification.data = doctor.certification
        form.emr.data = doctor.emr
        form.languages.data = doctor.languages
        form.salary_expectations.data = doctor.salary_expectations

        # Populate multi-select fields
        form.states_licensed.data = doctor.states_licensed.split(",") if doctor.states_licensed else []
        form.states_willing_to_work.data = doctor.states_willing_to_work.split(",") if doctor.states_willing_to_work else []

        # Populate Malpractice cases safely
        malpractice_cases = json.loads(doctor.malpractice_cases or '[]')
        form.malpractice_cases.entries.clear()
        for case in malpractice_cases[:form.malpractice_cases.max_entries]:
            form.malpractice_cases.append_entry({
                'incident_year': case.get('incident_year', ''),
                'outcome': case.get('outcome', ''),
                'payout_amount': case.get('payout_amount', 0)
            })
        while len(form.malpractice_cases.entries) < form.malpractice_cases.min_entries:
            form.malpractice_cases.append_entry()

        # Populate Fellowship fields safely
        fellowships = doctor.fellowship.split(",") if doctor.fellowship else []
        fellowship_dates = doctor.fellowship_grad_month_year.split(",") if doctor.fellowship_grad_month_year else []

        form.fellowship.entries.clear()
        for fellowship in fellowships:
            form.fellowship.append_entry(fellowship)
        while len(form.fellowship.entries) < form.fellowship.min_entries:
            form.fellowship.append_entry()

        form.fellowship_grad_month_year.entries.clear()
        for date in fellowship_dates:
            form.fellowship_grad_month_year.append_entry(date)
        while len(form.fellowship_grad_month_year.entries) < form.fellowship_grad_month_year.min_entries:
            form.fellowship_grad_month_year.append_entry()



    return render_template('edit_doctor.html', form=form, doctor=doctor)


with app.app_context():
    db.create_all()  # <-- Create tables first!

    # Check if admin already exists to avoid duplicates
    existing_admin = User.query.filter_by(username='adminchan').first()

    if not existing_admin:
        admin = User(
            username='adminchan',
            email='admin@example.com',
            password_hash=generate_password_hash('icecream2'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user 'adminchan' created successfully!")
    else:
        print("Admin user already exists.")
# App initialization
threading.Thread(target=lambda: (time.sleep(1), webbrowser.open('http://localhost:5000'))).start()

@app.route('/reset_db')
def reset_db():
    db.drop_all()
    db.create_all()
    return "✅ Database has been reset!"

with app.app_context():
    db.create_all()

    doctors = Doctor.query.all()
    print("Existing Doctors and Emails:")
    for doc in doctors:
        print(doc.first_name, doc.last_name, doc.email)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
