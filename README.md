# Workout Application Backend

## About

This project comprises of a workout tracking system that allows users to create, view, and manage workouts and exercises. The application supports linking exercises to workouts with additional details such as reps, sets, and duration. Overall the system includes (but is not limited to):
- A Flask-based REST API with CRUD operations for workouts and exercises.
- A join table to associate exercises with workouts, including reps, sets, and duration.
- Data validation at the schema, model, and database levels.
- A seed file to populate the database with example data.

## File Structure

The following file/folder structure is (within `server`):
- [app.py](/server/app.py): contains backend routes and view functions for performing operations on workouts and exercises
- [models.py](/server/models.py): contains database models, relationships, constraints, validations, and schemas
- [seed.py](/server/seed.py): contains logic to populate the database with initial data
- [migrations](/server/migrations/): contains database migration files

## Project Use

To use this repository:

### Installation

Clone the repository:
```sh
git clone https://github.com/aneeshkodali/fis-se-course-9-module-8-summative-lab-flask-sqlalchemy.git
```

Make sure you are in the root repository:
```sh
cd fis-se-course-9-module-8-summative-lab-flask-sqlalchemy
```

Install necessary libraries:
```sh
pipenv install
```

Activate virtual environment:
```sh
pipenv shell
```

Switch to the `server` directory:
```sh
cd server
```

Run database migrations:
```sh
flask db upgrade
```

Seed the database:
```sh
python seed.py
```

### Server

Run the server:
```sh
python app.py
```

The server will run on:
http://127.0.0.1:5555

## API Endpoints

### GET /workouts
Returns all workouts

### GET /workouts/<id>
Returns a single workout by ID, including associated exercises and workout details

### POST /workouts
Creates a new workout

Request body:
{
  "date": "2024-04-01",
  "duration_minutes": 30,
  "notes": "Morning workout"
}

### DELETE /workouts/<id>
Deletes a workout by ID

### GET /exercises
Returns all exercises

### GET /exercises/<id>
Returns a single exercise by ID, including associated workouts

### POST /exercises
Creates a new exercise

Request body:
{
  "name": "Push Ups",
  "category": "Strength",
  "equipment_needed": false
}

### DELETE /exercises/<id>
Deletes an exercise by ID

### POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Associates an exercise with a workout and includes additional details

Request body:
{
  "reps": 10,
  "sets": 3,
  "duration_seconds": 60
}
