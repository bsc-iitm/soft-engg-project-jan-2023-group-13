from flask import current_app as app
from flask import jsonify, request, send_file, current_app

import bcrypt


from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)

jwt = JWTManager(app)

from datetime import datetime


salt = bcrypt.gensalt()


@app.post("/login")
def login():
    # Getting user Creds
    userdata = request.get_json()
    user_name = userdata["username"]
    password = userdata["password"].encode()
    access_token = create_access_token(identity=1)
    return jsonify(access_token=access_token)

    # Getting Creds from db
    curr_user = User.query.filter_by(username=user_name).first()

    # checking creds
    if curr_user is None:
        return jsonify({"msg": "Bad username"})
    elif bcrypt.checkpw(password, curr_user.password):
        # Creating JWT token
        cache.clear()
        access_token = create_access_token(identity=curr_user.id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad password"})


# Create User
@app.post("/register")
def register():
    # Getting data
    userdata = request.get_json()
    usr = User.query.filter_by(username=userdata["username"]).first()
    em = User.query.filter_by(email=userdata["email"]).first()

    if usr or em:
        return jsonify("User already Exists")
    password = userdata["password"].encode()

    # Hashing Password
    hashed_pass = bcrypt.hashpw(password, salt)

    # commiting Data
    db.session.add(
        User(
            username=userdata["username"], email=userdata["email"], password=hashed_pass
        ),
    )
    db.session.commit()
    return jsonify("Success")


@app.get("/home")
@jwt_required()
def home():
    return get_jwt_identity()


# @app.get("/login")
# def login():
#     return "welcome to login page"


# @app.post("/register")
# def register():
#     tracker_data = request.get_json()
#     return tracker_data
