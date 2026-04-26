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

    return jsonify(WorkoutSchema(many=True).dump(Workout.query.all())), 200

@app.route('/workouts/<int:id>')
def get_workout(id):

    # query for workout
    workout = Workout.query.get(id)

    # return error if not found
    if not workout:
        msg = {'error': f"Workout with ID {id} not found"}
        return jsonify(msg), 404
    
    return jsonify(WorkoutSchema().dump(workout)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():

    try:

        # get data from request
        data = WorkoutSchema().load(request.get_json())
        workout = Workout(**data)

        # commit
        db.session.add(workout)
        db.session.commit()

        # return
        return jsonify({'id': workout.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

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
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


    # return
    return jsonify({'message': f"Workout with ID {workout.id} deleted"}), 200

@app.route('/exercises', methods=['GET'])
def get_exercises():

    return jsonify(ExerciseSchema(many=True).dump(Exercise.query.all())), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):

    # query for exercise
    exercise = Exercise.query.get(id)

    # return error if not found
    if not exercise:
        msg = {'error': f"Exercise with ID {id} not found"}
        return jsonify(msg), 404
    
    return jsonify(ExerciseSchema().dump(exercise)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():

    try:

        # get data from request
        data = ExerciseSchema().load(request.get_json())
        exercise = Exercise(**data)

        # commit
        db.session.add(exercise)
        db.session.commit()

        # return
        return jsonify({'id': exercise.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

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

    # retrieve objects
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    # return early if objects not found
    if not workout:
        return jsonify({'error': f"Workout with ID {workout_id} not found"}), 404
    
    if not exercise:
        return jsonify({'error': f"Exercise with ID {exercise_id} not found"}), 404

    try:
        # get data from request
        data = WorkoutExerciseSchema().load(request.get_json())
        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            **data
        )

        # commit
        db.session.add(workout_exercise)
        db.session.commit()

        # return
        return jsonify(WorkoutExerciseSchema().dump(workout_exercise)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)