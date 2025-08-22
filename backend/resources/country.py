
from flask_restful import Resource, marshal_with, abort
from parsers import country_args
from models import CountryModel
from serializers import country_fields, countries_fields
from sqlalchemy.exc import IntegrityError
from config import db


class CountriesResource(Resource):
    @marshal_with(countries_fields)
    def get(self):
        all_countries = CountryModel.query.all()
        return all_countries

    @marshal_with(country_fields)
    def post(self):
        args = country_args.parse_args()
        new_country = CountryModel(
            name=args["name"]
        )
        try:
            db.session.add(new_country)
            db.session.commit()
            return new_country, 201
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Country name already exists")
        except Exception as error:
            db.session.rollback()
            abort(500, message="An unexpected error ocurred")


class CountryResource(Resource):
    @marshal_with(country_fields)
    def get(self, id):
        country = CountryModel.query.filter_by(id=id).first()
        if not country:
            abort(404, message=f"Country with ID {id} not found")
        return country

    @marshal_with(country_fields)
    def patch(self, id):
        country = CountryModel.query.filter_by(id=id).first()
        if not country:
            abort(404, message=f"Country with ID {id} not found")

        args = country_args.parse_args()

        for key, value in args.items():
            setattr(country, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update Country: {e}")
        return country

    def delete(self, id):
        country = CountryModel.query.filter_by(id=id).first()
        if not country:
            abort(404, message=f"Country with ID {id} not found")
        db.session.delete(country)
        db.session.commit()
        return "", 204
