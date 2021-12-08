# import flask for web application 
from flask import Flask
# import flask sqlalchemy to enable ORM and link it with flask
from flask_sqlalchemy import SQLAlchemy

# define flask application 
app = Flask(__name__)

# setup application configuration with database
# config string: dialect :// username : password @ host address : port number / dbname
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:csci@localhost:5432/tigerclaws'

# link a database instance using SQLAlchemy with flask application
db = SQLAlchemy(app)

# create person class using db.Model (create and manipulate data models)
class Person(db.Model):
  __tablename__ = 'persons'  # specify table name
  id = db.Column(db.Integer, primary_key = True) # specific each column
  name = db.Column(db.String(), nullable = False)

# detects models and creates tables for them (if they don't exist)
db.create_all()

# add person
person1 = Person(name='John')
db.session.add(person1)
db.session.commit()
# setup the route so it directs the user to the homepage
@app.route('/')
# the route handler will be called index
def index():

    # simple return
    #return "Hello, this is a test!"

    # return name example, same as select
    person = Person.query.first()
    return 'Hello ' + person.name + '!'