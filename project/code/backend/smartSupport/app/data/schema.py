from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "email", "first_name", "last_name")