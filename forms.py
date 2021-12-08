from datetime import datetime, time
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.fields.datetime import TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, AnyOf, URL

class CourseForm(Form):
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
    isAvail = BooleanField(
        'isAvail', validators=[DataRequired()]
    )

