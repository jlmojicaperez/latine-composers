# imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from datetime import datetime

# class Base(DeclarativeBase):
#   pass
# 
# db = SQLAlchemy(model_class=Base)

# Create app
app = Flask(__name__)
# configure SQLite database relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# initialize app with the extension
#db.init_app(app)
#db = SQLAlchemy(model_class=Base)
db = SQLAlchemy(app)

composer_genre_association = db.Table(
    'composer_genre_association',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True),
    db.Column('composer_id', db.Integer, db.ForeignKey('composer.composer_id'), primary_key=True)
)

class Genre(db.Model):
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    composers = db.relationship("Composer", secondary=composer_genre_association,
                                backref=db.backref("genres", lazy="dynamic"))

    def __repr__(self):
        return f"Genre Name: {self.name}, ID: {self.genre_id}.\nDescription: {self.description}"

class Composer(db.Model):
    __tablename__ = "composer"

    composer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    image = db.Column(db.String(200))
    country_of_birth = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))
    birth_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime)
    sex = db.Column(db.String(20))
    country_of_education = db.Column(db.String(20))
    sample_link = db.Column(db.String(200))
    sample_title = db.Column(db.String(100))
    website = db.Column(db.String(100))
    email = db.Column(db.String(100))
    more_info = db.Column(db.String(100))

    def __repr__(self):
        return f"Composer: {self.name}, ID: {self.composer_id}"


@app.get("/")
def index():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/composers")
def composers():
    try:
        composers_list = Composer.query.order_by(Composer.name).all()
        print(composers_list)
        return render_template("composers.html", composers_list=composers_list)
    except Exception as e:
        return f"ERROR {e}"

@app.get("/genres")
def genres():
    try:
        genres_list = Genre.query.order_by(Genre.name).all()
        print(genres_list)
        return render_template("genres.html", genres_list=genres_list)
    except Exception as e:
        return f"ERROR {e}"

# TODO: make a route and template to show the genre details

@app.get("/profile/<int:composer_id>")
def profile(composer_id):
    composer = Composer.query.get(composer_id)
    return render_template("profile.html", composer=composer)

@app.post("/create_genre")
def create_genre_post():
    genre = Genre(
        name = request.form["name"],
        description = request.form["description"],
    )
    print(genre)
    try:
        db.session.add(genre)
        db.session.commit()
        return redirect("/create_genre")
    except Exception as e:
        return f"ERROR {e}"

@app.get("/create_genre")
def create_genre_get():
    return render_template("create_genre.html")


@app.get("/create_composer")
def create_composer_get():
    genres = Genre.query.order_by(Genre.name)
    return render_template("create_composer.html", genres=genres)



@app.post("/create_composer")
def create_composer_post():
    # add composer
    composer = Composer(
        name = request.form["name"],
        image = request.form["image"],
        country_of_birth = request.form["country_of_birth"],
        ethnicity = request.form["ethnicity"],
        birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d"),
        death_date = datetime.strptime(request.form["death_date"], "%Y-%m-%d"),
        sex = request.form["sex"],
        country_of_education = request.form["country_of_education"],
        # TODO: Fix the way genre's are added to a composer
        genres = request.form["genres"],
        sample_link = request.form["sample_link"],
        sample_title = request.form["sample_title"],
        website = request.form["website"],
        email = request.form["email"],
        more_info = request.form["more_info"],
    )
    try:
        db.session.add(composer)
        db.session.commit()
        return redirect("/create_composer")
    except Exception as e:
        print(f"ERROR {e}")
        return f"ERROR {e}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)