from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "email", "first_name", "last_name")


class TicketSchema(ma.Schema):
    class Meta:
        fields = ("ticket_id", "student_id", "title", "body", "status",
                  "votes_count", "created_at", "updated_at")