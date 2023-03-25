import bcrypt, uuid
from datetime import datetime

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
from app.data.models import Ticket, Vote
from app.data.schema import TicketSchema
from app.utils.validation import *

jwt = JWTManager(app)
salt = bcrypt.gensalt()

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)


@app.get("/api/tickets")
def get_tickets():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))

    vote_subquery = db.session.query(
            Vote.ticket_id, func.count(Vote.vote_id).label('vote_count')
        ).group_by(Vote.ticket_id).subquery()

    sorted_tickets = Ticket.query.join(
        vote_subquery, Ticket.ticket_id == vote_subquery.c.ticket_id).order_by(
        Ticket.status.asc(), Ticket.created_at.asc(), vote_subquery.c.vote_count.desc()
        ).limit(per_page).offset(page*per_page).all()

    result = tickets_schema.dump(sorted_tickets)
    return jsonify(result), 200


@app.post("/api/tickets")
@jwt_required()
def post_ticket():
    current_user_id = get_jwt_identity()
    ticketdata = request.get_json()

    title = ticketdata['title']
    body = ticketdata['body']

    Validation.is_valid_string_value(title, 'Title', alpha_only=False)
    Validation.is_valid_string_value(body, 'Blog Body', alpha_only=False, allow_special_chars=True)

    body = Markup(body)

    new_ticket = Ticket(title=title, body=body, student_id=current_user_id)
    db.session.add(new_ticket)
    db.session.commit()

    return ticket_schema.jsonify(new_ticket), 200