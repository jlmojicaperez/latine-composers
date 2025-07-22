
export default function ComposerProfile({ composer }) {
  let default_image_id = 1
  if (composer === null) {
    composer = {
      "first_name": "",
      "last_name": "",
      "image": { "image_id": default_image_id },
      "birth_date": "",
      "death_date": "",
      "gender": { "name": "" },
      "ethnicity": "",
      "country_of_birth": { "name": "" },
      "country_of_education": { "name": "" },
      "website": "",
      "email": "",
      "more_info": "",
      "tags": []
    }
  }
  return <form>
    <label for="first_name">First Name: </label>
    <input type="text" id="first_name" name="first_name" placeholder={composer.first_name} />
    <label for="last_name">Last Name: </label>
    <input type="text" id="last_name" name="last_name" placeholder={composer.last_name} />
    <img src={`http://localhost:8080/api/images/${composer.image.image_id}`} style={{ height: "128px" }} />
    <label for="img_file">Image file: </label>
    <input type="file" id="image_file" name="image_file" />
    <label for="birth_date">Born: </label>
    <input type="date" id="birth_date" name="birth_date" value={composer.birth_date} />
    <label for="death_date">Died: </label>
    <input type="date" id="death_date" name="death_date" value={composer.death_date} />
    <label for="gender:">Gender:</label>
    <input type="text" id="gender.name" name="gender.name" value={composer.gender.name} />
    <label for="ethnicity">Ethnicity:</label>
    <input type="text" id="ethnicity" name="ethnicity" value={composer.ethnicity} />
    <label for="country_of_birth">Country of Birth:</label>
    <input type="text" id="country_of_birth.name" name="country_of_birth.name" value={composer.country_of_birth.name} />
    <label for="country_of_education">Country of Education:</label>
    <input type="text" id="country_of_education.name" name="country_of_education.name" value={composer.country_of_education.name} />
    <label for="website">Website:</label>
    <input type="text" id="website" name="website" value={composer.website} />
    <label for="email">Email:</label>
    <input type="text" id="email" name="email" value={composer.email} />
    <label for="more_info">More Info: {composer.more_info}</label>
    {composer.tags.map((tag) => (
      <span key={tag.tag_id}>{tag.name}</span>
    ))}
  </form>
}

