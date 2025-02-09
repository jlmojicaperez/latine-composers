# imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

# app 
app = Flask(__name__)

# TODO: SQLAlchemy Extension
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/composers")
def composers():
    return render_template("composers.html")


@app.route("/profile/<composer_id>")
def profile(composer_id):
    # fetch data from the database
    composer_data = composers_db.get(composer_id)
    return render_template("profile.html", composer=composer_data)

if __name__ == "__main__":
    app.run(debug=True)