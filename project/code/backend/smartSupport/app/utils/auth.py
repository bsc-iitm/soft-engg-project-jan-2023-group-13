import json, re
from werkzeug.exceptions import HTTPException
from flask import make_response

from app.data.models import User
from app.data.db import db


class NotAuthorized(HTTPException):
    def __init__(self):
        self.response = make_response(
            json.dumps('You are Not Authorized to perform this action'), 401)


class Auth():
    def authorize(current_user_id, resource_id):
        if str(current_user_id) != str(resource_id):
            raise NotAuthorized()