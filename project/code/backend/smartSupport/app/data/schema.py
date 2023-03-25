from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.data.models import Comment

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "email", "first_name", "last_name")


class TicketSchema(ma.Schema):
    class Meta:
        fields = ("ticket_id", "title", "body", "status", "votes_count", "student",
                  "created_at", "updated_at")

    student = ma.Nested(UserSchema)


class CommentSchema(ma.Schema):
    class Meta:
        # model = Comment
        fields = ("comment_id", "body", "created_at", "updated_at", 'commentor')

    commentor = ma.Nested(UserSchema)
