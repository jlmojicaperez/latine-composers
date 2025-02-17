# imports
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from datetime import datetime

# test data
composers_db = {
    "beethoven": {
        "name": "Ludwig van Beethoven",
        "image": "images/beethoven.jpg",  
        "country_of_birth": "Germany",
        "ethnicity": "German",
        "birth_date": "December 1770",
        "death_date": "March 26, 1827",
        "sex": "Male",
        "country_of_education": "Austria",
        "genres": ["Classical", "Symphony", "Piano Concerto"],
        "sample_link": "https://youtu.be/3ug835LFixU?si=Rt6sTrIH9skXGE0C",
        "sample_title": "Beethoven: Symphony No. 5 | Herbert Blomstedt and the Gewandhausorchester Leipzig",
        "website": "https://www.example.com/beethoven",
        "email": "beethoven@example.com",
        "more_info": "A great composer..."
    },
    # ... more composers ...
}


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# Create app
app = Flask(__name__)
# configure SQLite database relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# initialize app with the extension
db.init_app(app) 

class Composer(db.Model):
    composer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    image = db.Column(db.String(200))
    country_of_birth = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))
    birth_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime)
    sex = db.Column(db.String(20))
    country_of_education = db.Column(db.String(20))
    genres = db.Column(db.String(20))
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
        composers = Composer.query.order_by(Composer.name).all()
        return render_template("composers.html", composers=composers)
    except Exception as e:
        return f"ERROR {e}"

@app.get("/profile/<int:composer_id>")
def profile(composer_id):
    # fetch data from the database
    composer = Composer.query.get(composer_id)
    return render_template("profile.html", composer=composer)

@app.get("/create")
def create_get():
    return render_template("create.html")

@app.post("/create")
def create_post():
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
        # TODO: Find way to make genres a list of values
        genres = request.form["genres"],
        sample_link = request.form["sample_link"],
        sample_title = request.form["sample_title"],
        website = request.form["website"],
        email = request.form["email"],
        more_info = request.form["more_info"],
    )
    print(type(composer.birth_date))
    try:
        db.session.add(composer)
        db.session.commit()
        return redirect("/create")
    except Exception as e:
        print(f"ERROR {e}")
        return f"ERROR {e}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)