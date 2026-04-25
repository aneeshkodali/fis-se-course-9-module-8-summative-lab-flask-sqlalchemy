from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, server_default=db.func.now())
    duration_minutes = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String)

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True),
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False),
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False),
    reps = db.Column(db.Integer, nullable=False),
    sets = db.Column(db.Integer, nullable=False),
    duration_seconds = db.Column(db.Integer, nullable=False)

