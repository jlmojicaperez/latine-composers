from flask_restful import Resource, marshal_with, abort
from parsers import tag_args, tag_update_args
from models import TagModel
from serializers import tag_fields, tags_fields
from sqlalchemy.exc import IntegrityError
from flask import request
from config import db


class TagsResource(Resource):
    @marshal_with(tags_fields)
    def get(self):
        all_tags = TagModel.query.all()
        return all_tags

    @marshal_with(tag_fields)
    def post(self):
        args = tag_args.parse_args()
        new_tag = TagModel(
            name=args["name"],
            description=args.get("description")
        )
        try:
            db.session.add(new_tag)
            db.session.commit()
            return new_tag, 201
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Tag name already exists")
        except Exception as error:
            db.session.rollback()
            abort(500, message=f"An unexpected error ocurred:\n{error}")


class TagResource(Resource):
    @marshal_with(tag_fields)
    def get(self, id):
        tag = TagModel.query.filter_by(id=id).first()
        if not tag:
            abort(404, message=f"Tag with ID {id} not found")
        return tag

    @marshal_with(tag_fields)
    def patch(self, id):
        try:
            raw_data = request.get_json(silent=True)
            if raw_data is None:
                abort(400, message="Invalid. JSON body required for PATCH request.")
        except Exception as e:
            # Catch potential issues during JSON parsing
            abort(400, message=f"Error parsing JSON body: {e}")

        tag = TagModel.query.filter_by(id=id).first()
        if not tag:
            abort(404, message=f"Tag with ID {id} not found")

        args = tag_update_args.parse_args()
        print(args)

        for key, value in args.items():
            # Check if the key was present in the request JSON body and only updates the ones that are
            if key in raw_data:
                setattr(tag, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update tag: {e}")
        return tag

    def delete(self, id):
        tag = TagModel.query.filter_by(id=id).first()
        if not tag:
            abort(404, message=f"Tag with ID {id} not found")
        db.session.delete(tag)
        db.session.commit()
        return "", 204
