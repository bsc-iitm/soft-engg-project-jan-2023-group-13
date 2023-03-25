import bcrypt, uuid
from datetime import datetime
from werkzeug.exceptions import Unauthorized

from sqlalchemy import desc, func
from flask import current_app as app
from flask import jsonify, request, Markup
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)

from app.data.db import db
from app.data.models import Ticket, Comment
from app.data.schema import CommentSchema
from app.utils.validation import *
from app.utils.auth import Auth

jwt = JWTManager(app)
salt = bcrypt.gensalt()

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


@app.get("/api/tickets/<ticket_id>/comments")
@jwt_required()
def get_comments(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if ticket:
        comments = db.session.query(Comment).filter(Comment.ticket_id == ticket_id).order_by(
                Comment.created_at.desc()).all()
        return comments_schema.jsonify(comments), 200
    else:
        raise NotFound(status_code=404, msg='Ticket not found')


@app.post("/api/tickets/<ticket_id>/comments")
@jwt_required()
def post_comment(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket:
        current_user_id = get_jwt_identity()
        commentdata = request.get_json()
        body = commentdata['body']
        Validation.is_valid_string_value(body, 'Comment Body', alpha_only=False,
                                        allow_special_chars=True)
        body = Markup(body)

        new_comment = Comment(body=body, ticket_id=ticket_id, user_id=current_user_id)
        db.session.add(new_comment)
        db.session.commit()
        return comment_schema.jsonify(new_comment), 200
    else:
        raise NotFound(status_code=404, msg='Ticket not found')


@app.get("/api/comments/<comment_id>")
@jwt_required()
def get_comment(comment_id):
    comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        return comment_schema.jsonify(comment), 200
    else:
        raise NotFound(status_code=404, msg='Comment not found')


@app.put("/api/comments/<comment_id>")
@jwt_required()
def put_comment(comment_id):
    current_user_id = get_jwt_identity()
    comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
    if comment:
        Auth.authorize(current_user_id, comment.user_id)
        return comment_schema.jsonify(comment), 200
    else:
        raise NotFound(status_code=404, msg='Comment not found')

