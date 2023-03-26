from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.data.models import Comment

ma = Marshmallow(app)


class RoleSchema(ma.Schema):
    class Meta:
        fileds = ("role_id", "name")


class UserSchema(ma.Schema):
    roles = ma.Nested(RoleSchema, many=True)

    class Meta:
        fields = ("user_id", "username", "email", "first_name", "last_name", "roles")


class TicketSchema(ma.Schema):
    class Meta:
        fields = (
            "ticket_id",
            "title",
            "body",
            "status",
            "votes_count",
            "student",
            "created_at",
            "updated_at",
        )

    student = ma.Nested(UserSchema)


class CommentSchema(ma.Schema):
    class Meta:
        # model = Comment
        fields = (
            "comment_id",
            "body",
            "created_at",
            "updated_at",
            "solution",
            "commentor",
        )

    commentor = ma.Nested(UserSchema)
