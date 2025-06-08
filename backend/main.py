from config import api, app, db
from resources.tag import TagResource, TagsResource
from resources.gender import GenderResource, GendersResource
from resources.country import CountryResource, CountriesResource
from resources.composer import ComposerResource, ComposersResource
import os

api.add_resource(ComposersResource, "/api/composers")
api.add_resource(ComposerResource, "/api/composers/<int:id>")
api.add_resource(CountriesResource, "/api/countries")
api.add_resource(CountryResource, "/api/countries/<int:id>")
api.add_resource(GendersResource, "/api/genders")
api.add_resource(GenderResource, "/api/genders/<int:id>")
api.add_resource(TagsResource, "/api/tags")
api.add_resource(TagResource, "/api/tags/<int:id>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
