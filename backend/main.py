from flask_restful import Resource, marshal_with, abort
from parsers import composer_args, tag_args, country_args, gender_args
from models import ComposerModel, TagModel, CountryModel, GenderModel
from config import api, app, db
from serializers import composer_fields, country_fields, tag_fields, gender_fields
from sqlalchemy.exc import IntegrityError
import os

class CountriesResource(Resource):
    @marshal_with(country_fields)
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

class ComposersResource(Resource):
    @marshal_with(composer_fields)
    def get(self):
        all_composers = ComposerModel.query.all()
        return all_composers

    @marshal_with(composer_fields)
    def post(self):
        args = composer_args.parse_args()
        new_composer = ComposerModel(
            first_name=args["first_name"],
            last_name=args["last_name"],
            image_url=args.get("image_url"),
            country_of_birth_id=args["country_of_birth_id"],
            birth_date=args.get("birth_date"),
            death_date=args.get("death_date"),
            gender_id=args.get("gender_id"),
            country_of_education_id=args.get("country_of_education"),
            sample_url=args.get("sample_url"),
            sample_title=args.get("sample_title"),
            website=args.get("website"),
            email=args.get("email"),
            more_info=args.get("more_info")
        )
        db.session.add(new_composer)
        db.session.commit()
        return new_composer, 201

class ComposerResource(Resource):
    @marshal_with(composer_fields)
    def patch(self, id):
        args = composer_args.parse_args()
        composer = ComposerModel.query.filter_by(composer_id=id).first()
        if not composer:
            abort(404, "Composer not found")
        composer.first_name = args["first_name"],
        composer.last_name = args["last_name"],
        composer.image_url = args.get("image_url"),
        composer.country_of_birth_id = args["country_of_birth_id"],
        composer.birth_date = args.get("birth_date"),
        composer.death_date = args.get("death_date"),
        composer.gender_id = args.get("gender_id"),
        composer.country_of_education_id = args.get("country_of_education"),
        composer.sample_url = args.get("sample_url"),
        composer.sample_title = args.get("sample_title"),
        composer.website = args.get("website"),
        composer.email = args.get("email"),
        composer.more_info = args.get("more_info")
        
        db.session.commit()
        return composer

    def delete(self, id):
        composer = ComposerModel.query.filter_by(composer_id=id).first()
        if not composer:
            abort(404, "Composer not found")
        db.session.delete(composer)
        db.session.commit()
        return composer

api.add_resource(ComposersResource, "/api/composers")
api.add_resource(ComposerResource, "/api/composers/<int:id>")
api.add_resource(CountriesResource, "/api/countries")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
