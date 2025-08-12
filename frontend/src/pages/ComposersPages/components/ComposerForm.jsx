import TagsSearchField from "./TagsSearchField"
import { useState } from "react"


export default function ComposerForm({ composer }) {
  let default_image_id = 1;
  const default_composer = {
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
  };

  const [myComposer, setMyComposer] = useState(composer ? composer : default_composer);

  function addTag(tag) {
    const tagFound = myComposer.tags.find((composerTag) => composerTag.tag_id === tag.tag_id);
    if (!!!tagFound) {
      setMyComposer({ ...myComposer, tags: [...myComposer.tags, tag] });
    }
  }
  function removeTag(tag) {
    let newTags = [];
    for (let index = 0; index < myComposer.tags.length; index++) {
      if (myComposer.tags[index].tag_id != tag.tag_id) {
        newTags.push(myComposer.tags[index]);
      }
    }
    setMyComposer({ ...myComposer, tags: newTags });
  }

  return <form>
    <label for="first_name">First Name: </label>
    <input type="text" id="first_name" name="first_name" placeholder={myComposer.first_name} /><br />
    <label for="last_name">Last Name: </label>
    <input type="text" id="last_name" name="last_name" placeholder={myComposer.last_name} /><br />
    <img src={`http://localhost:8080/api/images/${myComposer.image.image_id}`} style={{ height: "128px" }} /><br />
    <label for="img_file">Image file: </label>
    <input type="file" id="image_file" name="image_file" /><br />
    <label for="birth_date">Born: </label>
    <input type="date" id="birth_date" name="birth_date" placeholder={myComposer.birth_date} /><br />
    <label for="death_date">Died: </label>
    <input type="date" id="death_date" name="death_date" placeholder={myComposer.death_date} /><br />
    <label for="gender:">Gender:</label>
    <input type="text" id="gender.name" name="gender.name" placeholder={myComposer.gender.name} /><br />
    <label for="ethnicity">Ethnicity:</label>
    <input type="text" id="ethnicity" name="ethnicity" placeholder={myComposer.ethnicity} /><br />
    <label for="country_of_birth">Country of Birth:</label>
    <input type="text" id="country_of_birth.name" name="country_of_birth.name" placeholder={myComposer.country_of_birth.name} /><br />
    <label for="country_of_education">Country of Education:</label>
    <input type="text" id="country_of_education.name" name="country_of_education.name" placeholder={myComposer.country_of_education.name} /><br />
    <label for="website">Website:</label>
    <input type="text" id="website" name="website" placeholder={myComposer.website} /><br />
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" placeholder={myComposer.email} /><br />
    <label for="more_info">More Info: </label>
    <input type="text" id="more_info" name="more_info" placeholder={myComposer.more_info} /><br />
    {myComposer.tags.map((tag) => (
      <span key={tag.tag_id}>
        <button type="button" onClick={() => removeTag(tag)}>{tag.name}</button>
      </span>
    ))}
    <br />
    <TagsSearchField addTag={addTag} />
  </form>
}

