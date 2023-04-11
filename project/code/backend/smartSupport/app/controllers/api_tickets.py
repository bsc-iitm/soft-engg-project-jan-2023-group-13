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
from app.data.models import Ticket, Vote, Faqs, Comment, Tag
from app.data.schema import TicketSchema
from app.utils.validation import *
from app.utils.auth import Auth, NotAuthorized

# jwt = JWTManager(app)
# salt = bcrypt.gensalt()

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)


# get all tickets
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


# raise a new ticket
@app.post("/api/tickets")
@jwt_required()
def post_ticket():
    current_user_id = get_jwt_identity()
    ticketdata = request.get_json()

    title = ticketdata['title']
    body = ticketdata['body']
    tags = ticketdata['tags']

    Validation.is_valid_string_value(title, 'Title', alpha_only=False)
    Validation.is_valid_string_value(body, 'Ticket Body', alpha_only=False, allow_special_chars=True)

    body = Markup(body)

    new_ticket = Ticket(title=title, body=body, student_id=current_user_id)

    for tagname in tags:
        tag = db.session.query(Tag).filter(Tag.name == tagname).first()
        if not tag:
            return jsonify('Tag {} not found'.format(tagname))
        new_ticket.tags.append(tag)
        # print(tag)

    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 200


# get a ticket by its itcket_id
@app.get("/api/tickets/<ticket_id>")
@jwt_required()
def get_ticket(ticket_id):
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket:
        return ticket_schema.jsonify(ticket), 200
    else:
        raise NotFound(status_code=404, msg='Ticket not found')


# edit a ticket
@app.put("/api/tickets/<ticket_id>")
@jwt_required()
def put_ticket(ticket_id):
    current_user_id = get_jwt_identity()
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if ticket:
        Auth.authorize(current_user_id, ticket.student_id)
        ticketdata = request.get_json()
        title = ticketdata['title']
        body = ticketdata['body']

        Validation.is_valid_string_value(title, 'Title', alpha_only=False)
        Validation.is_valid_string_value(
            body, 'Blog Body', alpha_only=False, allow_special_chars=True)

        ticket.title = title
        ticket.body = Markup(body)
        db.session.add(ticket)
        db.session.commit()
        return ticket_schema.jsonify(ticket), 200
    else:
        raise NotFound(status_code=404, msg='Ticket not found')


# delete a ticket
@app.delete("/api/tickets/<ticket_id>")
@jwt_required()
def delete_ticket(ticket_id):
    current_user_id = get_jwt_identity()
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if str(ticket.student_id) != str(current_user_id):
        return jsonify("Not Authorized"), 401

    if ticket:
        db.session.delete(ticket)
        db.session.commit()
        return jsonify('Ticket Deleted'), 204
    else:
        raise NotFound(status_code=404, msg='Ticket not found')


# get tickets of a given user by username
@app.get("/api/tickets/user/<username>")
def get_user_tickets(username):
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))

    student = db.session.query(User).filter(User.username == username).first()

    vote_subquery = db.session.query(
            Vote.ticket_id, func.count(Vote.vote_id).label('vote_count')
        ).group_by(Vote.ticket_id).subquery()

    sorted_tickets = Ticket.query.join(
        vote_subquery, Ticket.ticket_id == vote_subquery.c.ticket_id,
        ).filter(Ticket.student_id == student.user_id).order_by(
        Ticket.status.asc(), Ticket.created_at.asc(), vote_subquery.c.vote_count.desc()
        ).limit(per_page).offset(page*per_page).all()

    result = tickets_schema.dump(sorted_tickets)
    return jsonify(result), 200


# close a ticket
@app.put("/api/tickets/<ticket_id>/close")
@jwt_required()
def close_ticket(ticket_id):
    current_user_id = get_jwt_identity()
    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

    if not Ticket:
        raise NotFound(status_code=404, msg='Ticket not found')

    if ticket.status == "Resolved":
        return jsonify("Ticket already resolved"), 400

    if Auth.authorize_support(current_user_id) or Auth.authorize_admin(current_user_id):
        ticket.status = "Closed"
        db.session.add(ticket)
        db.session.commit()
        return ticket_schema.jsonify(ticket), 200
    else:
        raise NotAuthorized()


# convert a resolved ticket to a FAQ
@app.post("/api/tickets/<ticket_id>/faqs")
@jwt_required()
def ticket_to_faq(ticket_id):
    current_user_id = get_jwt_identity()
    if not Auth.authorize_admin(current_user_id):
        raise NotAuthorized()

    ticket = db.session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket.status != "Resolved":
        return jsonify("Can convert unresolved ticket to FAQ"), 400

    comment = db.session.query(Comment).filter(
        Comment.ticket_id == ticket_id, Comment.solution==1).first()

    if not comment:
        return jsonify("Solution comment not found"), 404

    new_faq = Faqs(query=ticket.body, answer=comment.body)

    db.session.add(new_faq)
    db.session.commit()

    return jsonify(f"Ticket converted to FAQ successfully with faq_id {new_faq.faq_id}")

