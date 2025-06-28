from flask_restful import Resource, marshal_with, abort
from parsers import instrument_args
from models import InstrumentModel
from serializers import instrument_fields, instruments_fields
from sqlalchemy.exc import IntegrityError
from config import db


class InstrumentsResource(Resource):
    @marshal_with(instruments_fields)
    def get(self):
        all_instruments = InstrumentModel.query.all()
        return all_instruments

    @marshal_with(instrument_fields)
    def post(self):
        args = instrument_args.parse_args()
        new_instrument = InstrumentModel(
            name=args["name"]
        )
        try:
            db.session.add(new_instrument)
            db.session.commit()
            return new_instrument, 201
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Instreument name already exists")
        except Exception as error:
            db.session.rollback()
            abort(500, message=f"An unexpected error ocurred: {error}")


class InstrumentResource(Resource):
    @marshal_with(instrument_fields)
    def get(self, id):
        instrument = InstrumentModel.query.filter_by(instrument_id=id).first()
        if not instrument:
            abort(404, message=f"Instreument with ID {id} not found")
        return instrument

    @marshal_with(instrument_fields)
    def patch(self, id):
        instrument = InstrumentModel.query.filter_by(instrument_id=id).first()
        if not instrument:
            abort(404, message=f"Instreument with ID {id} not found")

        args = instrument_args.parse_args()

        for key, value in args.items():
            setattr(instrument, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Failed to update instrument: {e}")
        return instrument

    def delete(self, id):
        instrument = InstrumentModel.query.filter_by(instrument_id=id).first()
        if not instrument:
            abort(404, message=f"Instreument with ID {id} not found")
        db.session.delete(instrument)
        db.session.commit()
        return "", 204
