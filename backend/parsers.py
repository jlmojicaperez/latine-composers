from flask_restful import reqparse, inputs
import werkzeug
import werkzeug.datastructures

composer_args = reqparse.RequestParser()
composer_args.add_argument("first_name", type=str, required=True, help="First name cannot be blank")
composer_args.add_argument("last_name", type=str, required=True, help="Last name cannot be blank")
composer_args.add_argument("image_url", type=str, required=False)
composer_args.add_argument("country_of_birth_id", type=int, required=True, help="Country of birth ID cannot be blank")
composer_args.add_argument("birth_date", type=inputs.datetime_from_iso8601, required=False)
composer_args.add_argument("death_date", type=inputs.datetime_from_iso8601, required=False)
composer_args.add_argument("gender_id", type=int, required=False)
composer_args.add_argument("country_of_education_id", type=int, required=False)
composer_args.add_argument("sample_url", type=str, required=False)
composer_args.add_argument("sample_title", type=str, required=False)
composer_args.add_argument("email", type=str, required=False)
composer_args.add_argument("website", type=str, required=False)
composer_args.add_argument("more_info", type=str, required=False)
composer_args.add_argument("tag_ids", type=int, action="append", required=False)

composer_update_args = reqparse.RequestParser()
composer_update_args.add_argument("first_name", type=str, required=False)
composer_update_args.add_argument("last_name", type=str, required=False)
composer_update_args.add_argument("image_url", type=str, required=False)
composer_update_args.add_argument("country_of_birth_id", type=int, required=False)
composer_update_args.add_argument("birth_date", type=inputs.datetime_from_iso8601, required=False)
composer_update_args.add_argument("death_date", type=inputs.datetime_from_iso8601, required=False)
composer_update_args.add_argument("gender_id", type=int, required=False)
composer_update_args.add_argument("country_of_education_id", type=int, required=False)
composer_update_args.add_argument("sample_url", type=str, required=False)
composer_update_args.add_argument("sample_title", type=str, required=False)
composer_update_args.add_argument("email", type=str, required=False)
composer_update_args.add_argument("website", type=str, required=False)
composer_update_args.add_argument("more_info", type=str, required=False)

tag_args = reqparse.RequestParser()
tag_args.add_argument("name", type=str, required=True, help="Name cannot be blank")
tag_args.add_argument("description", type=str, required=False)

tag_update_args = reqparse.RequestParser()
tag_update_args.add_argument("name", type=str, required=False)
tag_update_args.add_argument("description", type=str, required=False)

country_args = reqparse.RequestParser()
country_args.add_argument("name", type=str, required=True, help="Name cannot be blank")

gender_args = reqparse.RequestParser()
gender_args.add_argument("name", type=str, required=True, help="Name cannot be blank")

image_args = reqparse.RequestParser()
image_args.add_argument("image_file", type=werkzeug.datastructures.FileStorage, location= "files", required=True, help="An image file is required")