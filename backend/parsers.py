from flask_restful import reqparse, inputs
from werkzeug.datastructures import FileStorage

composer_args = reqparse.RequestParser()
composer_args.add_argument("first_name", type=str,
                           required=True, help="First name cannot be blank")
composer_args.add_argument("last_name", type=str,
                           required=True, help="Last name cannot be blank")
composer_args.add_argument("image", required=False)
composer_args.add_argument(
    "birth_date", type=inputs.datetime_from_iso8601, required=False)
composer_args.add_argument(
    "death_date", type=inputs.datetime_from_iso8601, required=False)
composer_args.add_argument("gender_id", type=int, required=False)
composer_args.add_argument("ethnicity_id", type=int, required=False)
composer_args.add_argument("country_of_birth", required=True,
                           help="Country of birth cannot be blank")
composer_args.add_argument("country_of_education", required=False)
composer_args.add_argument("sample_url", type=str, required=False)
composer_args.add_argument("sample_title", type=str, required=False)
composer_args.add_argument("email", type=str, required=False)
composer_args.add_argument("website", type=str, required=False)
composer_args.add_argument("more_info", type=str, required=False)
composer_args.add_argument("tags", action="append", required=False)

composer_update_args = reqparse.RequestParser()
composer_update_args.add_argument("first_name", type=str, required=False)
composer_update_args.add_argument("last_name", type=str, required=False)
composer_update_args.add_argument("image", required=False)
composer_update_args.add_argument(
    "birth_date", type=inputs.datetime_from_iso8601, required=False)
composer_update_args.add_argument(
    "death_date", type=inputs.datetime_from_iso8601, required=False)
composer_update_args.add_argument("gender", required=False)
composer_update_args.add_argument("ethnicity", required=False)
composer_update_args.add_argument("country_of_birth", required=False)
composer_update_args.add_argument("country_of_education", required=False)
composer_update_args.add_argument("sample_url", type=str, required=False)
composer_update_args.add_argument("sample_title", type=str, required=False)
composer_update_args.add_argument("email", type=str, required=False)
composer_update_args.add_argument("website", type=str, required=False)
composer_update_args.add_argument("more_info", type=str, required=False)
composer_update_args.add_argument("tags", action="append", required=False)

tag_args = reqparse.RequestParser()
tag_args.add_argument("name", type=str, required=True,
                      help="Name cannot be blank")
tag_args.add_argument("description", type=str, required=False)

tag_update_args = reqparse.RequestParser()
tag_update_args.add_argument("name", type=str, required=False)
tag_update_args.add_argument("description", type=str, required=False)

country_args = reqparse.RequestParser()
country_args.add_argument(
    "name", type=str, required=True, help="Name cannot be blank")

gender_args = reqparse.RequestParser()
gender_args.add_argument("name", type=str, required=True,
                         help="Name cannot be blank")

ethnicity_args = reqparse.RequestParser()
ethnicity_args.add_argument(
    "name", type=str, required=True, help="Name cannot be blank")

instrument_args = reqparse.RequestParser()
instrument_args.add_argument(
    "name", type=str, required=True, help="Name cannot be blank")

image_args = reqparse.RequestParser()
image_args.add_argument("image_file", type=FileStorage, location="files",
                        required=True, help="An image file is required")
