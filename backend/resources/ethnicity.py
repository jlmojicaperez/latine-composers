from flask_restful import Resource, marshal_with, abort
from parsers import ethnicity_args
from models import EthnicityModel
from serializers import ethnicity_fields, ethnicities_fields
from sqlalchemy.exc import IntegrityError
from config import db


class EthnicitiesResource(Resource):
    @marshal_with(ethnicities_fields)
    def get(self):
        all_ethnicities = EthnicityModel.query.all()
        return all_ethnicities

    @marshal_with(ethnicity_fields)
    def post(self):
        args = ethnicity_args.parse_args()
        new_ethnicity = EthnicityModel(
            name=args["name"]
        )
        try:
            db.session.add(new_ethnicity)
            db.session.commit()
            return new_ethnicity, 201
        except IntegrityError:
            db.session.rollback()
            abort(409, message="ethnicity name already exists")
        except Exception as error:
            db.session.rollback()
            abort(500, message=f"An unexpected error ocurred: {error}")


class EthnicityResource(Resource):
    @marshal_with(ethnicity_fields)
    def get(self, id):
        ethnicity = EthnicityModel.query.filter_by(id=id).first()
        if not ethnicity:
            abort(404, message=f"ethnicity with ID {id} not found")
        return ethnicity

    @marshal_with(ethnicity_fields)
    def patch(self, id):
        ethnicity = EthnicityModel.query.filter_by(id=id).first()
        if not ethnicity:
            abort(404, message=f"ethnicity with ID {id} not found")

        args = ethnicity_args.parse_args()

        for key, value in args.items():
            setattr(ethnicity, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update ethnicity: {e}")
        return ethnicity

    def delete(self, id):
        ethnicity = EthnicityModel.query.filter_by(id=id).first()
        if not ethnicity:
            abort(404, message=f"ethnicity with ID {id} not found")
        db.session.delete(ethnicity)
        db.session.commit()
        return "", 204
