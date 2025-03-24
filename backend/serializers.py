from flask_restful import fields

composer_fields = {
    "composer_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "image_url": fields.String,
    "country_of_birth_id": fields.Integer,
    "country_of_birth": fields.String,
    "birth_date": fields.DateTime(dt_format="iso8601"),
    "death_date": fields.DateTime(dt_format="iso8601"),
    "gender_id": fields.Integer,
    "gender": fields.String,
    "country_of_education_id": fields.Integer,
    "country_of_education": fields.String,
    "sample_url": fields.String,
    "sample_title": fields.String,
    "website": fields.String,
    "email": fields.String,
    "more_info": fields.String
    }

tag_fields = {
    "tag_id": fields.Integer,
    "name": fields.String,
    "description": fields.String
}

country_fields = {
    "country_id": fields.Integer,
    "name": fields.String,
}

gender_fields = {
    "gender_id": fields.Integer,
    "name": fields.String,
}

