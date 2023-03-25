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

jwt = JWTManager(app)
salt = bcrypt.gensalt()

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


@app.get("/api/tickets/<ticket_id>/comments")
@jwt_required()
def get_comments(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if ticket:
        comments = db.session.query(Comment).filter(Comment.ticket_id == ticket_id).all()
        return comments_schema.jsonify(comments), 200
    else:
        raise NotFound(status_code=404, msg='Ticket not found')