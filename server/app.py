from flask import Flask, make_response, jsonify, request
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

    # initialize workouts list
    workouts = []

    # loop through Workouts and return dict
    for workout in Workout.query.all():
        workouts.append({
            'id': workout.id,
            'date': workout.date,
            'duration_minutes': workout.duration_minutes,
            'notes': workout.notes,
        })

    # return list
    return jsonify(workouts), 200

@app.route('/workouts/<id>:int')
def get_workout(id):

    # query for workout
    workout = Workout.query.filter(Workout.id == id).first()

    # return error if not found
    if not workout:
        msg = {'error': f"Workout with ID {id} not found"}
        return make_response(msg, 404)
    
    # return workout
    workout_dict = {
        'id': workout.id,
        'date': workout.date,
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
        duration_minutes=data.get('duration_minutes')
        notes=data.get('notes')
    )

    # commit
    db.session.add(workout)
    db.session.commit()

    # return
    return jsonify({'id': workout.id}), 201

@app.route('/workouts/<id>:int', methods=['DELETE'])
def delete_workout(id):

    # query for workout
    workout = Workout.query.filter(Workout.id == id).first()

    # return error if not found
    if not workout:
        msg = {'error': f"Workout with ID {id} not found"}
        return make_response(msg, 404)
    
    # commit
    db.session.delete(workout)
    db.session.commit()

    # return
    return jsonify({'message': f"Workout with ID {workout.id} deleted"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)