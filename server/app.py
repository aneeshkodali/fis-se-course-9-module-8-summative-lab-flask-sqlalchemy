from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route('/workouts', methods=['GET'])
def get_workouts():

    # loop through Workouts and return dict
    workouts = [
        {
            'id': workout.id,
            'date': str(workout.date),
            'duration_minutes': workout.duration_minutes,
            'notes': workout.notes,
        }
        for workout in Workout.query.all()
    ]

    # return list
    return jsonify(workouts), 200

@app.route('/workouts/<int:id>')
def get_workout(id):

    # query for workout
    workout = Workout.query.get(id)

    # return error if not found
    if not workout:
        msg = {'error': f"Workout with ID {id} not found"}
        return jsonify(msg), 404
    
    # return workout
    workout_dict = {
        'id': workout.id,
        'date': str(workout.date),
        'duration_minutes': workout.duration_minutes,
        'notes': workout.notes,
        'exercises': [
            {
                'id': exercise.id,
                'name': exercise.name,
            }
            for exercise in workout.exercises
        ]
    }
    return jsonify(workout_dict), 200

@app.route('/workouts', methods=['POST'])
def create_workout():

    # get data from request
    data = request.get_json()
    
    # create new workout object
    workout = Workout(
        date=data.get('date'),
        duration_minutes=data.get('duration_minutes'),
        notes=data.get('notes')
    )

    # commit
    try:
        db.session.add(workout)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    # return
    return jsonify({'id': workout.id}), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):

    # query for workout
    workout = Workout.query.get(id)

    # return error if not found
    if not workout:
        msg = {'error': f"Workout with ID {id} not found"}
        return jsonify(msg), 404
    
    # commit
    try:
        db.session.delete(workout)
        db.session.commit()
    except Exception as e:


    # return
    return jsonify({'message': f"Workout with ID {workout.id} deleted"}), 200

@app.route('/exercises', methods=['GET'])
def get_exercises():

    # loop through Exercises and return dict
    exercises = [
        {
            'id': exercise.id,
            'name': exercise.name,
            'category': exercise.category,
            'equipment_needed': exercise.equipment_needed,
        }
        for exercise in Exercise.query.all()
    ]
    
    # return list
    return jsonify(exercises), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):

    # query for exercise
    exercise = Exercise.query.get(id)

    # return error if not found
    if not exercise:
        msg = {'error': f"Exercise with ID {id} not found"}
        return jsonify(msg), 404
    
    # return exercise
    exercise_dict = {
        'id': exercise.id,
        'name': exercise.name,
        'category': exercise.category,
        'equipment_needed': exercise.equipment_needed,
        'workouts': [
            {
                'id': workout.id,
                'date': str(workout.date),
            }
            for workout in exercise.workouts
        ]
    }
    return jsonify(exercise_dict), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():

    # get data from request
    data = request.get_json()
    
    # create new exercise object
    exercise = Exercise(
        name=data.get('name'),
        category=data.get('category'),
        equipment_needed=data.get('equipment_needed')
    )

    # commit
    try:
        db.session.add(exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    # return
    return jsonify({'id': exercise.id}), 201

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):

    # query for exercise
    exercise = Exercise.query.get(id)

    # return error if not found
    if not exercise:
        msg = {'error': f"Exercise with ID {id} not found"}
        return jsonify(msg), 404
    
    # commit
    try:
        db.session.delete(exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    # return
    return jsonify({'message': f"Exercise with ID {exercise.id} deleted"}), 200

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):

    # get data from request
    data = request.get_json()

    # retrieve objects
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    # return early if objects not found
    if not workout:
        return jsonify({'error': f"Workout with ID {workout_id} not found"}), 404
    elif not exercise:
        return jsonify({'error': f"Exercise with ID {exercise_id} not found"}), 404

    # create object
    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )

    # commit
    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    

    return jsonify({'message': "Exercise added to workout"}), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)