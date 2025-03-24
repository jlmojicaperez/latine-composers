# imports
import os
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create app
app = Flask(__name__)
# configure SQLite database relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# initialize app with the extension
db = SQLAlchemy(app)

composer_tag_association = db.Table(
    'composer_tag_association',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True),
    db.Column('composer_id', db.Integer, db.ForeignKey('composer.composer_id'), primary_key=True)
)

class Country(db.Model):
    __tablename__ = "country"

    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

class Tag(db.Model):
    __tablename__ = "tag"

    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    composers = db.relationship("Composer", secondary=composer_tag_association,
                                backref=db.backref("tags", lazy="dynamic"))

    def __repr__(self):
        return f"tag Name: {self.name}, ID: {self.tag_id}"

class Composer(db.Model):
    __tablename__ = "composer"

    composer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    image = db.Column(db.String(200))
    country_of_birth = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))
    birth_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime)
    sex = db.Column(db.String(20))
    country_of_education = db.Column(db.String(20))
    sample_url = db.Column(db.String(200))
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

@app.get("/tags")
def tags():
    tags_list = Tag.query.order_by(Tag.name).all()
    return render_template("tags.html", tags_list=tags_list)

@app.get("/tag/<int:tag_id>")
def tag_details(tag_id):
    tag = tag.query.get(tag_id)
    return render_template("tag_details.html", tag=tag)

@app.get("/create_tag")
def create_tag_get():
    return render_template("create_tag.html")

@app.post("/create_tag")
def create_tag_post():
    tag = tag(
        name = request.form["name"],
        description = request.form["description"],
    )
    print(tag)
    try:
        db.session.add(tag)
        db.session.commit()
        return redirect("/create_tag")
    except Exception as e:
        return f"ERROR {e}"

@app.delete("/delete_tag/<int:tag_id>")
def delete_tag(tag_id):
    tag = tag.query.filter_by(tag_id=tag_id).first()
    try:
        db.session.delete(tag)
        db.session.commit()
        return redirect("/tags")
    except Exception as e:
        return f"ERROR {e}"
    

@app.get("/composers")
def composers():
    composers_list = Composer.query.order_by(Composer.last_name).all()
    return render_template("composers.html", composers_list=composers_list)

@app.get("/composer/<int:composer_id>")
def composer_details(composer_id):
    composer = Composer.query.get(composer_id)
    return render_template("composer_details.html", composer=composer)

@app.get("/create_composer")
def create_composer_get():
    tags = Tag.query.order_by(Tag.name).all()
    print(tags)
    return render_template("create_composer.html", tags=tags)

@app.post("/create_composer")
def create_composer_post():
    # add composer
    composer = Composer(
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        image = request.form["image"],
        country_of_birth = request.form["country_of_birth"],
        ethnicity = request.form["ethnicity"],
        birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d"),
        death_date = datetime.strptime(request.form["death_date"], "%Y-%m-%d"),
        sex = request.form["sex"],
        country_of_education = request.form["country_of_education"],
        sample_link = request.form["sample_link"],
        sample_title = request.form["sample_title"],
        website = request.form["website"],
        email = request.form["email"],
        more_info = request.form["more_info"],
    )
    # Get selected tag IDs from the form
    tag_ids = request.form.getlist("tags_select")
    selected_tags = []
    if tag_ids:
        # Retrieve tag objects from the database based on IDs
        selected_tags = Tag.query.filter(Tag.tag_id.in_(tag_ids)).all()
        # Associate selected tags with the composer
        composer.tags.extend(selected_tags)
    print(selected_tags)

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

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))