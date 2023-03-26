from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.data.db import db
from app.data.models import Faqs, Tag
from app.data.schema import FaqsSchema

from app.utils.validation import *
from app.utils.auth import Auth, NotAuthorized


@app.get("/api/faqs")
def get_faqs():
    faq_list = Faqs.query.order_by(Faqs.faq_id).all()

    faq_schema = FaqsSchema(many=True)
    output = faq_schema.dump(faq_list)
    return jsonify(output)
