
from flask_restful import Resource, marshal_with, abort
from parsers import composer_args, composer_update_args
from models import ComposerModel, TagModel, CountryModel, GenderModel
from serializers import composer_fields, composers_fields
from flask import request
from config import db

class ComposersResource(Resource):
    @marshal_with(composers_fields)
    def get(self):
        all_composers = ComposerModel.query.all()
        return all_composers

    @marshal_with(composer_fields)
    def post(self):
        args = composer_args.parse_args()
        raw_data = None
        try:
            raw_data = request.get_json(silent=True)
            if raw_data is None:
                abort(400, message="Invalid. JSON body required for PATCH request.")
        except Exception as e:
            # Catch potential issues during JSON parsing
             abort(400, message=f"Error parsing JSON body: {e}")

        country_of_birth = CountryModel.query.filter_by(country_id=args["country_of_birth_id"]).first()
        if not country_of_birth:
            abort(404, message=f"Country with ID {args["country_of_birth_id"]} not found")

        country_of_education = None
        if "country_of_education_id" in raw_data:
            country_of_education = CountryModel.query.filter_by(country_id=args["country_of_education_id"]).first()
            if not country_of_education:
                abort(404, message=f"Country with ID {args["country_of_education_id"]} not found")

        gender = None
        if "gender_id" in raw_data:
            gender = GenderModel.query.filter_by(gender_id=args["gender_id"]).first()
            if not gender:
                abort(404, message=f"Gender with ID {args["gender_id"]} not found")

        tags = []
        for id in args["tag_ids"]:
            tag = TagModel.query.filter_by(tag_id=id).first()
            if not tag:
                abort(404, message=f"Tag with ID {id} not found")
            tags.append(tag)


        new_composer = ComposerModel(
                first_name=args["first_name"],
                last_name=args["last_name"],
                image_url=args.get("image_url"),
                birth_date=args.get("birth_date"),
                death_date=args.get("death_date"),
                sample_url=args.get("sample_url"),
                sample_title=args.get("sample_title"),
                website=args.get("website"),
                email=args.get("email"),
                more_info=args.get("more_info"),
                gender=gender,
                country_of_birth=country_of_birth,
                country_of_education=country_of_education,
                tags=tags
                )

        db.session.add(new_composer)
        db.session.commit()
        return new_composer, 201

class ComposerResource(Resource):
    @marshal_with(composer_fields)
    def patch(self, id):
        try:
            raw_data = request.get_json(silent=True)
            if raw_data is None:
                abort(400, message="Invalid. JSON body required for PATCH request.")
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