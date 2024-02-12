"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Usuario,Personajes,Planetas,Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body),   200

# this only runs if `$ python src/app.py` is executed

@app.route("/usuario", methods=["POST"])
def create_user():
    body = request.json
    name = body.get("name")
    email = body.get("email")
    password = body.get("password")
    
    if email is None or password is None or name is None:
        return jsonify({
            "message": "Email, password and name are required"
        }), 400
    
    user_exist = Usuario.query.filter_by(email=email).one_or_none()
    if user_exist is not None:
        return jsonify({
            "message": "User already exists"
        }), 400
    user = Usuario(email, password, name)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ocurrió un error interno",
            "error": error.args
        }), 500
    return jsonify({}), 201

@app.route("/usuario", methods=["GET"])
def get_all_user():
    
    user = Usuario.query.all()
    print("esto es user",user)
    if user is None:

         return jsonify(""), 404
    usuario=[fav.serialize() for fav in user]

    return jsonify(usuario), 200

@app.route("/planetas", methods=["GET"])
def get_all_planets():
    
    valor = Planetas.query.all()
   
    if valor is None:

         return jsonify(""), 404
    planetas=[fav.serialize() for fav in valor]

    return jsonify(planetas), 200

@app.route("/personajes", methods=["GET"])
def get_all_personajes():
    
    valor = Personajes.query.all()
    
    if valor is None:

         return jsonify(""), 404
    planetas=[fav.serialize() for fav in valor]

    return jsonify(planetas), 200

@app.route("/usuario/<int:id>", methods=["GET"])
def get_user(id):
    if id is None: 
        return jsonify({
            "message": "id is required"
        }), 400
    user = Usuario.query.get(id)
    if user is None:

         return jsonify(""), 404
    return jsonify(user.serialize()), 200


@app.route("/personajes", methods=["POST"])
def create_personaje():
    body = request.json
    name = body.get("name")
    person_class = body.get("person_class")
    faccion = body.get("faccion")
    race = body.get("race")
    gender = body.get("gender")
    
    if person_class is None or faccion is None or race is None or gender is None or name is None:
        return jsonify({
            "message": "All information are required"
        }), 400
    
    personajes = Personajes(
    faccion=faccion,
    person_class=person_class,
    race=race,
    gender=gender,
    name=name
    )

    try:
        db.session.add(personajes)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ocurrió un error interno",
            "error": error.args
        }), 500
    return jsonify({}), 201


@app.route("/personajes/<int:id>", methods=["GET"])
def get_personaje(id):
    if id is None: 
        return jsonify({
            "message": "id is required"
        }), 400
    personaje = Personajes.query.get(id)
    if personaje is None:
         return jsonify(""), 404
    return jsonify(personaje.serialize()), 200


@app.route("/planetas", methods=["POST"])
def create_planeta():
    body = request.json
    name = body.get("name")
    size = body.get("size")
    temp = body.get("temp")
    color = body.get("color")
    moon_numbers = body.get("moon_numbers")
    
    if name is None or size is None or temp is None or color is None or moon_numbers is None:
        return jsonify({
            "message": "All information are required"
        }), 400
    
    planetas = Planetas(
    moon_numbers=moon_numbers,
    size=size,
    temp=temp,
    color=color,
    name= name
    )

    try:
        db.session.add(planetas)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ocurrió un error interno",
            "error": error.args
        }), 500
    return jsonify({}), 201

@app.route("/planetas/<int:id>", methods=["GET"])
def get_planetas(id):
    if id is None: 
        return jsonify({
            "message": "id is required"
        }), 400
    planetas = Planetas.query.get(id)
    if  planetas is None:
         return jsonify(""), 404
    return jsonify( planetas.serialize()), 200

@app.route("/usuario/<int:id>/favoritos", methods=["GET"])
def get_favoritos(id):
    if id is None: 
        return jsonify({
            "message": "id is required"
        }), 400
    favorito = Usuario.query.get(id)
    if favorito is None:
         return jsonify(""), 404
    return jsonify({"favoritos":favorito.serialize()["favoritos"]}), 200
         
@app.route("/usuario/<int:user_id>/favoritos/planetas/<int:planet_id>", methods=["POST"])
def agregar_planeta(user_id,planet_id):
    
    body = request.json
    planeta=Planetas.query.get(planet_id)
    usuario=Usuario.query.get(user_id)

    
    if planeta is None or usuario is None:
        return jsonify({
            "message": "All information are required"
        }), 400
    
    favoritos = Favoritos(
        user_id=user_id,
        planet_id=planet_id
    )

    try:
        db.session.add(favoritos)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ocurrió un error interno",
            "error": error.args
        }), 500
    return jsonify({}), 201


@app.route("/usuario/<int:user_id>/favoritos/personajes/<int:personaje_id>", methods=["POST"])
def agregar_personaje(user_id,personaje_id):
    
    body = request.json
    personaje=Personajes.query.get(personaje_id)
    usuario=Usuario.query.get(user_id)

    
    if personaje is None or usuario is None:
        return jsonify({
            "message": "All information are required"
        }), 400
    
    favoritos = Favoritos(
        user_id=user_id,
        personaje_id=personaje_id
    )

    try:
        db.session.add(favoritos)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "message": "ocurrió un error interno",
            "error": error.args
        }), 500
    return jsonify({}), 201




@app.route("/usuario/<int:id>", methods=["DELETE"])
def delete_purchase_order(id):
    if id is None: 
        return jsonify({
            "message": "id is required"
        }), 400
    usuario = Usuario.query.get(id)
    print("wwwwwwwwwwwwwwwwwwwwww",usuario)
    if usuario is None:
        return jsonify(None), 404
    # Elimina la orden de la db. Revisa app.py el método delete_and_commit
    deleted = usuario.delete_and_commit()
    # Si la variable delted es False, quiere decir que no se guardó y ocurrió un error
    if not deleted:
        return jsonify({
            "message": "Something happened with db, try again"
        }), 500
    # Retorna status code indicando que todo salió bien, pero sin contenido
    # Revisar: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE#responses
    return jsonify(None), 204

@app.route("/usuario/<int:user_id>/favoritos/planetas/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id,user_id):
    if planet_id is None or user_id is None: 
        return jsonify({
            "message": "id is required"
        }), 400
    planet = Favoritos.query.filter_by(planet_id=planet_id, user_id=user_id).first()
    print("ffffffffffffffffffffffffffesto es planet",planet)
    if planet is None:
        return jsonify(None), 404
    # Elimina la orden de la db. Revisa app.py el método delete_and_commit
    deleted = Favoritos.delete(planet)
    # Si la variable delted es False, quiere decir que no se guardó y ocurrió un error
    if not deleted:
        return jsonify({
            "message": "Something happened with db, try again"
        }), 500
    # Retorna status code indicando que todo salió bien, pero sin contenido
    # Revisar: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE#responses
    return jsonify(None ), 204


@app.route("/usuario/<int:user_id>/favoritos/personajes/<int:personaje_id>", methods=["DELETE"])
def delete_personaje(personaje_id,user_id):
    if personaje_id is None or user_id is None: 
        return jsonify({
            "message": "id is required"
        }), 400
    personaje = Favoritos.query.filter_by(personaje_id=personaje_id, user_id=user_id).first()
    
    if personaje is None:
        return jsonify(None), 404
    # Elimina la orden de la db. Revisa app.py el método delete_and_commit
    deleted = Favoritos.delete(personaje)
    # Si la variable delted es False, quiere decir que no se guardó y ocurrió un error
    if not deleted:
        return jsonify({
            "message": "Something happened with db, try again"
        }), 500
    # Retorna status code indicando que todo salió bien, pero sin contenido
    # Revisar: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE#responses
    return jsonify(None), 204




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
