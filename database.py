import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.orm import interfaces, strategies, relationship
from interface import core
from db import db

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(core)
db.init_app(app)

migration = Migrate(app, db)

#Models

class Course(db.Model):
    __tablename__ = 'Course'
    id = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(50), nullable = True)
    hrs = db.Column(db.Integer, nullable = False)
    time = db.Column(db.Time, nullable = False)
    days = db.Column(db.String(50), nullable = False)
    faculty = db.Column(db.String(50), nullable = False)
    dept = db.Column(db.String(50), nullable = False)
    room = db.Column(db.String(50), nullable = False)
    isAvail = db.Column(db.Boolean, nullable = False)
    # schedule_name = db.Column(db.String(50), db.ForeignKey('Schedule.name'))
    #countsFor = relationship("Major", secondary = db.course_fullfills_major)

class Schedule(db.Model):
    __tablename__ = 'Schedule'
    name = db.Column(db.String(50), primary_key = True)
    semester = db.Column(db.String(50), nullable = False)
    # courses = relationship("Course")
    # student_id = db.Column(db.Integer, db.ForeignKey('Student.id'))

class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    year = db.Column(db.String(50), nullable = False)
    # schedules = relationship("Schedule")
    # majors = relationship("Major", secondary = db.students_major_in)

class Major(db.Model):
    __tablename__ = 'Major'
    name = db.Column(db.String(50), primary_key = True)
    dept = db.Column(db.String(50), nullable = False)
    core = db.Column(db.Integer, nullable = False)
    elec = db.Column(db.Integer, nullable = False)

students_major_in = db.Table('Majors In', db.Model.metadata,
    db.Column('student_id', db.Integer, db.ForeignKey('Student.id')),
    db.Column('major_name', db.String(50), db.ForeignKey('Major.name'))
)

course_fullfills_major = db.Table('Fullfills', db.Model.metadata,
    db.Column('course_id', db.String(50), db.ForeignKey('Course.id')),
    db.Column('major_name', db.String(50), db.ForeignKey('Major.name'))
)


#Courses

@app.route('/courses')
def courses():
  data = []

  return render_template('pages/courses.html')

@app.route('/courses/search', methods=['POST'])
def search_courses():
  results = Course.query.filter(Course.name.ilike('%{}%'.format(request.form['search_term']))).all()
  response={
    "count": len(results),
    "data": []
    }
  for course in results:
    response["data"].append({
        "id": course.id,
        "name": course.name,
        "num_upcoming_shows": course.upcoming_shows_count
      })
  
  return render_template('pages/search_courses.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/courses/<int:course_id>')
def show_course(course_id):
  course = Course.query.get(course_id)

  data={
    "id": course.id,
    "name": course.name,
    "hrs": course.hrs,
    "time": course.time,
    "days": course.days,
    "faculty": course.faculty,
    "dept": course.dept,
    "room": course.room,
    "isAvail": course.isAvail
  }
  return render_template('pages/show_course.html', course=data)

#Create Course
@app.route('/courses/create', methods=['GET'])
def create_course_form():
  form = CourseForm()
  return render_template('forms/new_course.html', form=form)

@app.route('/courses/create', methods=['POST'])
def create_coursenew_course_submission():
  new_course = Course()
  new_course.name = request.form['name']
  new_course.hrs = request.form['hrs']
  new_course.time = request.form['time']
  new_course.days = request.form['days']
  new_course.faculty = request.form['faculty']
  new_course.dept = request.form['dept']
  new_course.room = request.form['room']
  new_course.isAvail = request.form['isAvail']
  try:
    db.session.add(new_course)
    db.session.commit()
    flash('Course ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Course ' + request.form['name'] + ' could not be listed.')
    db.session.close()
  return redirect(url_for('index'))

#Delete Course
@app.route('/courses/delete', methods=['POST'])
def delete_course():
  course_id = request.form.get('course_id')
  deleted_course = Course.query.get(course_id)
  courseName = deleted_course.name
  try:
    db.session.delete(deleted_course)
    db.session.commit()
    flash('Course ' + courseName + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('please try again. Course ' + courseName + ' could not be deleted.')
  finally:
    db.session.close()
  return redirect(url_for('index'))

#Update Course
@app.route('/courses/edit', methods=['GET'])
def edit_course():
  course_id = request.args.get('course_id')
  form = CourseForm()
  course = Course.query.get(course_id)
  course_info={
    "id": course.id,
    "name": course.name,
    "hrs": course.hrs,
    "time": course.time,
    "days": course.days,
    "faculty": course.faculty,
    "dept": course.dept,
    "room": course.room,
    "isAvail": course.isAvail
  }
  return render_template('forms/edit_course.html', form=form, course=course_info)

@app.route('/courses/<int:course_id>/edit', methods=['POST'])
def edit_course_submission(course_id):
  course = Course.query.get(course_id)
  course.name = request.form['name']
  course.hrs = request.form['hrs']
  course.time = request.form['time']
  course.days = request.form['days']
  course.faculty = request.form['faculty']
  course.dept = request.form['dept']
  course.room = request.form['room']
  course.isAvail = request.form['isAvail']
  try:
    db.session.commit()
    flash('Course ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Course ' + course.name + ' could not be updated.')
  finally:
    db.session.close()
  return redirect(url_for('show_course', course_id=course_id))




# # course1 = Course(id = 'CSCI 3344', name = 'Database Systems', hrs = 3, time = '2:30', days = 'MWF', faculty = 'Dr. Tan', dept = 'Comp Sci', room = 'CSI 257', isAvail = True)
# # db.session.delete(course1)

# # student1 = Student(id = 830608, name = 'Justin Velasco', email = 'jvelasco@trinity.edu', year = 'Junior')
# # db.session.add(student1)

# # major1 = Major(name = 'Computer Science', dept = 'Computer Science', core = 0, elec = 0)
# # db.session.add(major1)

# #data = Course.query.all()


# #Errors
# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('errors/404.html'), 404

# @app.errorhandler(500)
# def server_error(error):
#     return render_template('errors/500.html'), 500

# with app.app_context():
#     db.create_all()
#     db.session.commit()

# if not app.debug:
#     file_handler = FileHandler('error.log')
#     file_handler.setFormatter(
#         Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
#     )
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('errors')

# Default port:
if __name__ == '__main__':
    app.run()

@app.route('/')
def index():
    course1 = Course.query.first()
    return 'Welcome to ' + course1.name + '!'