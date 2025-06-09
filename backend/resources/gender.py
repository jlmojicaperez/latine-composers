

from flask_restful import Resource, marshal_with, abort
from parsers import gender_args
from models import GenderModel
from serializers import gender_fields, genders_fields
from sqlalchemy.exc import IntegrityError
from config import db

class GendersResource(Resource):
    @marshal_with(genders_fields)
    def get(self):
        all_genders = GenderModel.query.all()
        return all_genders

    @marshal_with(gender_fields)
    def post(self):
        args = gender_args.parse_args()
        new_gender = GenderModel(
                name=args["name"]
                )
        try:
            db.session.add(new_gender)
            db.session.commit()
            return new_gender, 201
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Gender name already exists")
        except Exception as error:
            db.session.rollback()
            abort(500, message="An unexpected error ocurred")

class GenderResource(Resource):
    @marshal_with(gender_fields)
    def get(self, id):
        gender = GenderModel.query.filter_by(gender_id=id).first()
        if not gender:
            abort(404, message=f"Gender with ID {id} not found")
        return gender

    @marshal_with(gender_fields)
    def patch(self, id):
        gender = GenderModel.query.filter_by(gender_id=id).first()
        if not gender:
            abort(404, message=f"Gender with ID {id} not found")

        args = gender_args.parse_args()

        for key, value in args.items():
            setattr(gender, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update gender: {e}")
        return gender

    def delete(self, id):
        gender = GenderModel.query.filter_by(gender_id=id).first()
        if not gender:
            abort(404, message=f"Gender with ID {id} not found")
        db.session.delete(gender)
        db.session.commit()
        return "", 204
