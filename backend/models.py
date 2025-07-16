from config import db


class EthnicityModel(db.Model):
    __tablename__ = "ethnicity"
    ethnicity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class ImageModel(db.Model):
    __tablename__ = "image"
    image_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=False)


class CountryModel(db.Model):
    __tablename__ = "country"

    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class GenderModel(db.Model):
    __tablename__ = "gender"

    gender_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  unique=True, nullable=False)

    def __repr__(self):
        return self.name


class PieceTypeModel(db.Model):
    __tablename__ = "piece_type"

    piece_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  unique=True, nullable=False)

    def __repr__(self):
        return self.name


instrument_piece_association = db.Table(
    'instrument_piece_association',
    db.Column('piece_id', db.Integer, db.ForeignKey(
        'piece.piece_id'), primary_key=True),
    db.Column('instrument_id', db.Integer, db.ForeignKey(
        'instrument.instrument_id'), primary_key=True),
    db.Column("instrument_count", db.Integer,
              primary_key=False, nullable=False)
)


class InstrumentModel(db.Model):
    __tablename__ = "instrument"
    instrument_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return self.name


composer_piece_association = db.Table(
    'composer_piece_association',
    db.Column('piece_id', db.Integer, db.ForeignKey(
        'piece.piece_id'), primary_key=True),
    db.Column('composer_id', db.Integer, db.ForeignKey(
        'composer.composer_id'), primary_key=True)
)


class PieceModel(db.Model):
    __tablename__ = "piece"

    piece_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('piece_type.piece_type_id'))
    type = db.relationship("PieceTypeModel", foreign_keys=[
                           type_id], backref="pieces")
    composers = db.relationship("ComposerModel",
                                secondary=composer_piece_association,
                                backref=db.backref("pieces", lazy="dynamic"))
    instrumentation = db.relationship("InstrumentModel",
                                      secondary=instrument_piece_association,
                                      backref=db.backref("pieces", lazy="dynamic"))

    def __repr__(self):
        return self.name


composer_tag_association = db.Table(
    'composer_tag_association',
    db.Column('tag_id', db.Integer, db.ForeignKey(
        'tag.tag_id'), primary_key=True),
    db.Column('composer_id', db.Integer, db.ForeignKey(
        'composer.composer_id'), primary_key=True)
)


class TagModel(db.Model):
    __tablename__ = "tag"

    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=True)
    composers = db.relationship("ComposerModel",
                                secondary=composer_tag_association,
                                backref=db.backref("tags", lazy="dynamic"))

    def __repr__(self):
        return self.name


class ComposerModel(db.Model):
    __tablename__ = "composer"

    composer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), unique=False, nullable=False)
    last_name = db.Column(db.String(200), unique=False, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("image.image_id"))
    image = db.relationship("ImageModel", foreign_keys=[
                            image_id], backref="composer")
    country_of_birth_id = db.Column(
        db.Integer, db.ForeignKey("country.country_id"))
    country_of_birth = db.relationship("CountryModel",
                                       foreign_keys=[country_of_birth_id],
                                       backref="composers_born")
    ethnicity_id = db.Column(
        db.Integer, db.ForeignKey("ethnicity.ethnicity_id"))
    ethnicity = db.relationship("EthnicityModel",
                                foreign_keys=[ethnicity_id],
                                backref="composers")
    birth_date = db.Column(db.DateTime, unique=False, nullable=True)
    death_date = db.Column(db.DateTime, unique=False, nullable=True)
    gender_id = db.Column(db.Integer, db.ForeignKey("gender.gender_id"))
    gender = db.relationship("GenderModel", foreign_keys=[
                             gender_id], backref="composers")
    country_of_education_id = db.Column(
        db.Integer, db.ForeignKey("country.country_id"))
    country_of_education = db.relationship("CountryModel",
                                           foreign_keys=[
                                               country_of_education_id
                                           ],
                                           backref="composers_educated")
    sample_url = db.Column(db.String(200), unique=False, nullable=True)
    sample_title = db.Column(db.String(100), unique=False, nullable=True)
    website = db.Column(db.String(100), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    more_info = db.Column(db.String(100), unique=False, nullable=True)
