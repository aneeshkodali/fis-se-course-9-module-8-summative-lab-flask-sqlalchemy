from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # has many with WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    # has many with Workout (through WorkoutExercise)
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    # validation
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == '':
            raise ValueError('Exercise name must exist')
        return value
    
class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # has many WorkoutExercise
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    # has many with Exercise (through WorkoutExercise)
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    # validation
    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        if value <= 0:
            raise ValueError(f"{key} must be positive")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    # constraints
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
        db.CheckConstraint('reps > 0', name='check_reps_positive'),
        db.CheckConstraint('sets > 0', name='check_sets_positive'),
        db.CheckConstraint('duration_seconds > 0', name='check_duration_seconds_positive')
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)

    # belongs to Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')

    # belongs to Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # validation
    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive_number(self, key, value):
        if value is None or value <= 0:
            raise ValueError(f"{key} must be positive")
        return value
