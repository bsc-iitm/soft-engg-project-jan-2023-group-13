from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.data.db import db
from app.data.models import Faqs, Tag
from app.data.schema import FaqsSchema

from app.utils.validation import *
from app.utils.auth import Auth, NotAuthorized


# Get all faqs
@app.get("/api/faqs")
def get_faqs():
    faq_list = db.session.query(Faqs).all()

    faq_schema = FaqsSchema(many=True)
    output = faq_schema.dump(faq_list)
    return jsonify(output)


# get faq by id
@app.get("/api/faqs/<faq_id>")
def faq_byID(faq_id):
    faq = db.session.query(Faqs).filter_by(faq_id=1).first()
    faq_schema = FaqsSchema()
    output = faq_schema.dump(faq)
    return jsonify(output)
