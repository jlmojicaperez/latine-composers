from flask_restful import fields

countries_fields = {
    "country_id": fields.Integer,
    "name": fields.String,
}

genders_fields = {
    "gender_id": fields.Integer,
    "name": fields.String,
}

tags_fields = {
    "tag_id": fields.Integer,
    "name": fields.String,
}

image_fields = {
    "image_id": fields.Integer,
    "url": fields.String,
}

composers_fields = {
    "composer_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "image": fields.Nested(image_fields),
}

composer_fields = {
    "composer_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "image": fields.Nested(image_fields),
    "birth_date": fields.DateTime(dt_format="iso8601"),
    "death_date": fields.DateTime(dt_format="iso8601"),
    "country_of_birth": fields.Nested(countries_fields),
    "country_of_education": fields.Nested(countries_fields),
    "gender": fields.Nested(genders_fields),
    "sample_url": fields.String,
    "sample_title": fields.String,
    "website": fields.String,
    "email": fields.String,
    "more_info": fields.String,
    "tags": fields.List(cls_or_instance=fields.Nested(tags_fields))
}

tag_fields = {
    "tag_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "composers": fields.List(fields.Nested(composers_fields))
}

country_fields = {
    "country_id": fields.Integer,
    "name": fields.String,
    "composers_born": fields.List(cls_or_instance=fields.Nested(composers_fields)),
    "composers_educated": fields.List(cls_or_instance=fields.Nested(composers_fields))
}

gender_fields = {
    "gender_id": fields.Integer,
    "name": fields.String,
    "composers": fields.List(fields.Nested(composers_fields))
}

