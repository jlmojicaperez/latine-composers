from flask_restful import Resource, marshal_with, abort
from parsers import composer_args, composer_update_args
from models import ComposerModel, CountryModel, GenderModel, TagModel, ImageModel, EthnicityModel
from serializers import composer_fields, composers_fields
from flask import request
from config import db


def set_composer_data(composer, data_key, data_id, data_model, args):
    data = data_model.query.filter_by(id=data_id).firtst()
    if not data:
        abort(404, message=f"{data_key} with ID {data_id} not found")
    else:
        setattr(composer, data_key, data)


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

        new_composer = ComposerModel()
        set_composer_data(new_composer,
                          "country_of_birth",
                          "country_of_birth_id",
                          CountryModel,
                          args)
        abort(404)

        country_of_birth = CountryModel.query.filter_by(
            country_id=args["country_of_birth_id"]).first()
        if not country_of_birth:
            abort(404, message=f"Country with ID {
                  args["country_of_birth_id"]} not found")

        country_of_education = None
        if "country_of_education_id" in raw_data:
            country_of_education = CountryModel.query.filter_by(
                country_id=args["country_of_education_id"]).first()
            if not country_of_education:
                abort(404, message=f"Country with ID {
                      args["country_of_education_id"]} not found")

        gender = None
        if "gender_id" in raw_data:
            gender = GenderModel.query.filter_by(
                gender_id=args["gender_id"]).first()
            if not gender:
                abort(404, message=f"Gender with ID {
                      args["gender_id"]} not found")

        tags = []
        for arg_tag in args["tags"]:
            tag = TagModel.query.filter_by(tag_id=arg_tag["tag_id"]).first()
            if not tag:
                abort(404, message=f"Tag with ID {
                    tag["tag_id"]} not found")
            else:
                tags.append(tag)

        image = None
        if "image" in raw_data:
            image = ImageModel.query.filter_by(
                image_id=args["image"]["image_id"]).first()
            if not image:
                abort(404, message=f"Image with ID {
                      args["image"]["image_id"]} not found")

        new_composer = ComposerModel(
            first_name=args["first_name"],
            last_name=args["last_name"],
            birth_date=args.get("birth_date"),
            death_date=args.get("death_date"),
            sample_url=args.get("sample_url"),
            sample_title=args.get("sample_title"),
            website=args.get("website"),
            email=args.get("email"),
            more_info=args.get("more_info"),
            image=image,
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
    def get(self, id):
        composer = ComposerModel.query.filter_by(id=id).first()
        if not composer:
            abort(404, message=f"Composer with ID {id} not found")
        return composer

    @marshal_with(composer_fields)
    def patch(self, id):
        try:
            raw_data = request.get_json(silent=True)
            if raw_data is None:
                abort(400, message="Invalid. JSON body required for PATCH request.")
        except Exception as e:
            # Catch potential issues during JSON parsing
            abort(400, message=f"Error parsing JSON body: {e}")

        composer = ComposerModel.query.filter_by(id=id).first()
        if not composer:
            abort(404, message=f"Composer with ID {id} not found")

        args = composer_update_args.parse_args()

        if "country_of_birth" in raw_data:
            country_of_birth = CountryModel.query.filter_by(
                country_id=args["country_of_birth"]["country_id"]).first()
            if not country_of_birth:
                abort(404, message=f"Country with ID {
                    args["country_of_birth"]["country_id"]} not found")
            else:
                composer.country_of_birth = country_of_birth

        if "country_of_education" in raw_data:
            country_of_education = CountryModel.query.filter_by(
                country_id=args["country_of_educationd"]["country_id"]).first()
            if not country_of_education:
                abort(404, message=f"Country with ID {
                      args["country_of_education"]["country_id"]} not found")
            else:
                composer.country_of_education = country_of_birth

        if "gender" in raw_data:
            gender = GenderModel.query.filter_by(
                gender_id=args["gender"]["gender_id"]).first()
            if not gender:
                abort(404, message=f"Gender with ID {
                      args["gender"]["gender_id"]} not found")
            else:
                composer.gender = gender

        if "ethnicity_id" in raw_data:
            ethnicity = EthnicityModel.query.filter_by(
                ethnicity_id=args["ethnicity"]["ethnicity_id"]).first()
            if not ethnicity:
                abort(404, message=f"ethnicity with ID {
                      args["ethnicity"]["ethnicity_id"]} not found")
            else:
                composer.ethnicity = ethnicity

        if "tags" in raw_data:
            tags = []
            for arg_tag in args["tags"]:
                tag = TagModel.query.filter_by(
                    tag_id=arg_tag["tag_id"]).first()
                if not tag:
                    abort(404, message=f"Tag with ID {
                          arg_tag["tag_id"]} not found")
                else:
                    tags.append(tag)
            composer.tags = tags

        if "image" in raw_data:
            image = ImageModel.query.filter_by(
                image_id=args["image"]["image_id"]).first()
            if not image:
                abort(404, message=f"Image with ID {
                      args["image"]["image_id"]} not found")
            else:
                composer.image = image

        keys_to_skip = {
            "country_of_birth",
            "country_of_education",
            "ethnicity",
            "gender",
            "image",
            "tags"
        }
        for key, value in args.items():
            # Check if the key was present in the request JSON body
            # and only updates the ones that are
            if key in raw_data and key not in keys_to_skip:
                setattr(composer, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update composer: {e}")
        return composer

    def delete(self, id):
        composer = ComposerModel.query.filter_by(id=id).first()
        if not composer:
            abort(404, message=f"Composer with ID {id} not found")
        db.session.delete(composer)
        db.session.commit()
        return "", 204
