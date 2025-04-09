from flask_restful import Resource, marshal_with, abort
from parsers import composer_args, composer_update_args, tag_args, tag_update_args, country_args, gender_args
from models import ComposerModel, TagModel, CountryModel, GenderModel
from config import api, app, db
from serializers import composer_fields, country_fields, tag_fields, gender_fields
from sqlalchemy.exc import IntegrityError
from flask import request
import os

class TagsResource(Resource):
    @marshal_with(tag_fields)
    def get(self):
        all_tags = TagModel.query.all()
        return all_tags
    
    def post(self):
        args = tag_args
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
            abort(500, message="An unexpected error ocurred")

class TagResource(Resource):
    @marshal_with
    def put(self, id):
        try:
            raw_data = request.get_json(silent=True)
            if raw_data is None:
                 abort(400, message="Invalid. JSON body required for PUT request.")
        except Exception as e:
             # Catch potential issues during JSON parsing
             abort(400, message=f"Error parsing JSON body: {e}")
        
        tag = TagModel.query.filter_by(tag_id=id).first()
        if not tag:
            abort(404, message=f"Tag with ID {id} not found")
        
        args = tag_update_args.parse_args()

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
        tag = TagModel.query.filter_by(tag_id=id).first()
        if not tag:
            abort(404, message=f"Tag with ID {id} not found")
        db.session.delete(tag)
        db.session.commit()
        return "", 204

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

class CountryResource(Resource):
    @marshal_with
    def put(self, id):
        country = CountryModel.query.filter_by(country_id=id).first()
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
        country = CountryModel.query.filter_by(country_id=id).first()
        if not country:
            abort(404, message=f"Country with ID {id} not found")
        db.session.delete(country)
        db.session.commit()
        return "", 204

class GendersResource(Resource):
    @marshal_with(gender_fields)
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
            country_of_education_id=args.get("country_of_education_id"),
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
    def put(self, id):
        try:
            raw_data = request.get_json(silent=True)
            if raw_data is None:
                 abort(400, message="Invalid. JSON body required for PUT request.")
        except Exception as e:
             # Catch potential issues during JSON parsing
             abort(400, message=f"Error parsing JSON body: {e}")
    
        composer = ComposerModel.query.filter_by(composer_id=id).first()
        if not composer:
            abort(404, message=f"Composer with ID {id} not found")
        
        args = composer_update_args.parse_args()

        for key, value in args.items():
            # Check if the key was present in the request JSON body and only updates the ones that are
            if key in raw_data:
                setattr(composer, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update composer: {e}")
        return composer

    def delete(self, id):
        composer = ComposerModel.query.filter_by(composer_id=id).first()
        if not composer:
            abort(404, message=f"Composer with ID {id} not found")
        db.session.delete(composer)
        db.session.commit()
        return "", 204

api.add_resource(ComposersResource, "/api/composers")
api.add_resource(ComposerResource, "/api/composers/<int:id>")
api.add_resource(CountriesResource, "/api/countries")
api.add_resource(GendersResource, "/api/genders")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
