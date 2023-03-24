import bcrypt, uuid
from datetime import datetime

from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)


from app.data.db import db
from app.data.models import User
from app.data.schema import UserSchema

jwt = JWTManager(app)
salt = bcrypt.gensalt()

user_schema = UserSchema()

@app.post("/api/user/login")
def login():
    # Getting user Creds
    userdata = request.get_json()
    user_name = userdata["username"]
    password = userdata["password"].encode('utf-8')
    access_token = create_access_token(identity=1)
    # return jsonify(access_token=access_token)

    # Getting Creds from db
    curr_user = User.query.filter_by(username=user_name).first()

    # checking creds
    if curr_user is None:
        return jsonify({"msg": "Bad username"})
    elif bcrypt.checkpw(password, curr_user.password):
        # Creating JWT token
        # cache.clear()
        access_token = create_access_token(identity=curr_user.user_id)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad password"})



# Create User
@app.post("/api/user/register")
def register():
    # Getting data
    userdata = request.get_json()
    usr = User.query.filter_by(username=userdata["username"]).first()
    em = User.query.filter_by(email=userdata["email"]).first()

    if usr or em:
        return jsonify("User already Exists"), 409
    password = userdata["password"].encode('utf-8')

    # Hashing Password
    hashed_pass = bcrypt.hashpw(password, salt)

    fs_uniquifier = uuid.uuid4().hex

    new_user = User(
        username=userdata["username"], email=userdata["email"], password=hashed_pass,
        first_name=userdata["first_name"], last_name=userdata["last_name"],
        fs_uniquifier=fs_uniquifier,
    )

    # commiting Data
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)