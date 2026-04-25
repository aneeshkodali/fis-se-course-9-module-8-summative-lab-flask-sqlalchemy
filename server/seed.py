#!/usr/bin/env python3

from app import app
from datetime import date
from models import *

with app.app_context():

	# reset data and add new example data, committing to db
    
    print("Seeding database...")

    # clear tables (make sure WorkoutExercise goes first)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    # create exercises
    pushups = Exercise(
        name="Push Ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )

    db.session.add_all([pushups, squats, running])
    db.session.commit()

    # create workouts
    workout1 = Workout(
        date=date(2024, 4, 1),
        duration_minutes=30,
        notes="Morning workout"
    )

    workout2 = Workout(
        date=date(2024, 4, 2),
        duration_minutes=45,
        notes="Leg day"
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    # create workout exercises
    we1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        reps=15,
        sets=3,
        duration_seconds=60
    )

    we2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=running.id,
        reps=1,
        sets=1,
        duration_seconds=600
    )

    we3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=squats.id,
        reps=12,
        sets=4,
        duration_seconds=90
    )

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete.")