import os
import sys
import json
from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor, db
#from auth.auth import AuthError, requires_auth
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from flask_migrate import Migrate


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  #Migrate(app,db)

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization, true")
    response.headers.add("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS")
    return response


  @app.route("/")
  def handler():
    return jsonify({
      "success": True,
      'message': 'Working!'
    })

  # Movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    #Returns all movies

    movies = Movie.query.order_by(Movie.id).all()
    movies_list = []

    if len(movies) == 0:
      abort(404)

    else:
      for movie in movies:
        movies_list.append(movie.format())

    return jsonify({
      'success': True,
      # 'movies': current_movies,
      # 'total_movies': len(Movie.query.all()),
      'movies': movies_list
    })



  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
    #Adds new movies
    body = request.form
    new_title = body.get('title')
    new_release_date = body.get('release_date')

    try:
      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()
      return jsonify({
        'success': True,
        'created movie': movie.format()
      })
    except Exception as error:
      print(sys.exc_info)
      abort(422)



  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, id):
    #Updates movies
    body = request.form
    new_title = body.get('title')
    new_release_date = body.get('release_date')

    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie is None:
        abort(404)
      else:
        movie.title = new_title
        movie.release_date = new_release_date
        movie.update()

      return jsonify({
        'success': True,
        'movie': movie.format()
      })

    except Exception as error:
      print(sys.exc_info)
      abort(422)





  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_i):
    #Removes movies
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404)
      else:
        movie.delete()

      return jsonify({
        'success': True,
        'deleted': movie.format()
      }), 200

    except Exception as error:
      print(sys.exc_info)
      abort(422)



  # Actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    actors_list = []

    if len(actors) == 0:
      abort(404)
    else:
      for actor in actors:
        actors_list.append(actor.format())
    return jsonify({
      'success': True,
      'actors': actors_list
    })


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
    #Adds new actors
    body = request.form
    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')

    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()

      return jsonify({
        'success': True,
        'created actor': actor.format()
      })

    except Exception as error:
      print(sys.exc_info)
      abort(422)



  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):
    #Updates actors
    body = request.form
    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')

    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()

      if actor is None:
        abort(404)

      else:
        actor.name = new_name
        actor.age = new_age
        actor.gender = new_gender
        actor.update()

      return jsonify({
        'success': True,
        'actor': actor.format()

      })

    except Exception as error:
      print(sys.exc_info)
      abort(422)




  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    #Removes movies
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404)

      else:
        actor.delete()

      return jsonify({
        'success': True,
        'deleted': actor.format()
      }), 200
    except Exception as error:
      print(sys.exc_info)
      abort(422)




  # Error Handling
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": "Unauthorized"
    }), 401

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable entity"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "server error"
    }), 500

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


  return app

app = create_app()



# if __name__ == '__main__':
#     # APP.run(host='0.0.0.0', port=8080, debug=True)
#     app.debug = True
#     app.run()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=8080, debug=True)
    app.run(port=8080, debug=True)