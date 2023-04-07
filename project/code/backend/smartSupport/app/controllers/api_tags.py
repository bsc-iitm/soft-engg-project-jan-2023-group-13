from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.data.db import db
from app.data.models import Tag
from app.data.schema import TagSchema


# Get all tags
@app.get("/api/tags")
@jwt_required()
def get_all_tags():
    tag_lists = Tag.query.order_by(Tag.tag_id).all()

    tag_schema = TagSchema(many=True)
    output = tag_schema.dump(tag_lists)

    return jsonify(output)
