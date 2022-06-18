from flask import Flask

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/database"

mongo = PyMongo(app)


@app.route("/api", methods=['POST'])
def add_film():
    _json = request.json
    title = _json['title']
    desc = _json['description']
    rental_duration = _json['rental_duration']
    rental_rate = _json['rental_rate']
    length = _json['length']
    replacement_cost = _json['replacement_cost']
    rating = _json['rating']
    list_actors = _json['list_actors']

    if title and desc and rental_duration and rental_rate and length and replacement_cost and rating and list_actors and request.method == 'POST':
        id = mongo.db.film.insert_one({'title': title,
                                       'description': desc,
                                       'rental_duration': rental_duration,
                                       'rental_rate': rental_rate,
                                       'length': length,
                                       'replacement_cost': replacement_cost,
                                       'rating': rating,
                                       'list_actors': list_actors})

        resp = jsonify("Film inserted successfully.")

        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route("/api", methods=['GET'])
def get_films():
    films = mongo.db.film.find()
    resp = dumps(films)
    return resp


@app.route("/api/<string:fname>", methods=['GET'])
def get_film(fname):
    film = mongo.db.film.find_one({'title': fname})
    resp = dumps(film)
    return resp


@app.route("/api/<string:fname>", methods=['DELETE'])
def delete_film(fname):
    film = mongo.db.film.delete_one({'title': fname})

    resp = jsonify("Film "+fname+" Deleted successfully.")

    resp.status_code = 200
    return resp


@app.route("/api/<string:fname>", methods=['PATCH'])
def update_film(fname):
    _json = request.json
    title = _json['title']
    desc = _json['description']
    rental_duration = _json['rental_duration']
    rental_rate = _json['rental_rate']
    length = _json['length']
    replacement_cost = _json['replacement_cost']
    rating = _json['rating']
    list_actors = _json['list_actors']

    if title and desc and rental_duration and rental_rate and length and replacement_cost and rating and list_actors and request.method == 'PATCH':
        mongo.db.film.update_one({'title': fname},
                                 {'$set': {'description': desc,
                                           'rental_duration': rental_duration,
                                           'rental_rate': rental_rate,
                                           'length': length,
                                           'replacement_cost': replacement_cost,
                                           'rating': rating,
                                           'list_actors': list_actors}
                                  })
        resp = jsonify("Film Updated successfully.")

        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run(debug=True)
