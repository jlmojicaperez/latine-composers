from flask_restful import Resource, marshal_with, abort
from parsers import image_args
from models import ImageModel
from serializers import image_fields
from config import db, app, IMAGE_ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS

class ImagesResource(Resource):
    @marshal_with(image_fields)
    def get(self):
        all_images = ImageModel.query.all()
        return all_images
    
    @marshal_with(image_fields)
    def post(self):
        args = image_args.parse_args()
        image_file = args["image_file"] 
        image_filename = secure_filename(image_file.filename)
        if not allowed_file(image_filename):
            abort(400, "Image must be in one of the following formats: jpg, jpeg, png or gif")
        image_url = os.path.join(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
        image_file.save(image_url)
        new_image = ImageModel(
            url=image_url
        )
        try:
            db.session.add(new_image)
            db.session.commit()
            return new_image, 201
        except Exception as error:
            db.session.rollback()
            abort(500, message=f"An unexpected error ocurred: {error}")
    
class ImageResource(Resource):
    @marshal_with(image_fields)
    def get(self, id):
        image = ImageModel.query.filter_by(image_id=id).first()
        if not image:
            abort(404, message=f"Image with ID {id} not found")
        return image

    @marshal_with(image_fields)
    def patch(self, id):
        image = ImageModel.query.filter_by(image_id=id).first()
        if not image:
            abort(404, message=f"Image with ID {id} not found")

        args = image_args.parse_args()
        new_image_file = args["image_file"] 
        new_image_filename = secure_filename(new_image_file.filename)
        if not allowed_file(new_image_filename):
            abort(400, "Image must be in one of the following formats: jpg, jpeg, png or gif")
        new_image_url = os.path.join(os.path.join(app.config["UPLOAD_FOLDER"], new_image_filename))
        new_image_file.save(new_image_url)
        try:
            os.remove(image.url)
            image.url = new_image_url
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update image: {e}")
        return image

    def delete(self, id):
        image = ImageModel.query.filter_by(image_id=id).first()
        if not image:
            abort(404, message=f"Image with ID {id} not found")
        db.session.delete(image)
        db.session.commit()
        os.remove(image.url)
        return "", 204
