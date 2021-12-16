from datetime import datetime, time
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.fields.datetime import TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, AnyOf, URL
from db import db

class CourseForm(Form):
    schedule_id = StringField(
        'schedule_id'
    )
    courseNum = StringField(
        'courseNum', validators=[DataRequired()]
    )
    name = StringField(
        'name', validators=[DataRequired()]
    )
    hrs = IntegerField(
        'hrs', validators=[DataRequired()]
    )
    time = TimeField(
        'time', validators=[DataRequired()]
    )
    days = StringField(
        'days', validators=[DataRequired()]
    )
    faculty = StringField(
        'faculty', validators=[DataRequired()]
    )
    dept = StringField(
        'dept', validators=[DataRequired()]
    )
    room = StringField(
        'room', validators=[DataRequired()]
    )
    countsFor = StringField(
        'countsFor', validators=[DataRequired()]
    )
    isAvail = BooleanField(
        'isAvail', validators=[DataRequired()]
    )

class StudentForm(Form):
    stuId = IntegerField(
        'stuId', validators=[DataRequired()]
    )
    name = StringField(
        'name', validators=[DataRequired()]
    )
    email = StringField(
        'email', validators=[DataRequired()]
    )
    year = StringField(
        'year', validators=[DataRequired()]
    )
    majors = StringField(
        'majors', validators=[DataRequired()]
    )
    schedules = StringField(
        'schedules', validators=[DataRequired()]
    )

class MajorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    dept = StringField(
        'dept', validators=[DataRequired()]
    )
    core = IntegerField(
        'core', validators=[DataRequired()]
    )
    elec = IntegerField(
        'elec', validators=[DataRequired()]
    )

class ScheduleForm(Form):
    student_id = StringField(
        'student_id'
    )
    name = StringField(
        'name', validators=[DataRequired()]
    )
    semester = StringField(
        'semester', validators=[DataRequired()]
    )
    courses = StringField(
        'courses', validators=[DataRequired()]
    )