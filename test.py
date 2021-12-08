from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgressql://postgress:tdse1985@localhost:5432'

db = SQLAlchemy(app)

class ToDo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(), nullable = False)

    def __repre__(self):
        return f'<ToDo {self.id} {self.description}>'

db.create_all()

thing1 = ToDo(description = 'do homework')
db.session.add(thing1)
db.session.commit()

data = ToDo.query.all()