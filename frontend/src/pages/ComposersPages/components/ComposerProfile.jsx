
export default function ComposerProfile({ composer }) {
  console.log(composer)
  return <div>
    <h2>{composer.first_name} {composer.last_name}</h2>
    <img src={`http://localhost:8080/api/images/${composer.image.image_id}`} style={{ height: "128px" }} />
    <p><strong>Born:</strong> {composer.birth_date}</p>
    <p><strong>Died:</strong> {composer.death_date}</p>
    <p><strong>Gender:</strong> {composer.gender.name}</p>
    <p><strong>Ethnicity:</strong> {composer.ethnicity}</p>
    <p><strong>Country of Birth:</strong> {composer.country_of_birth.name}</p>
    <p><strong>Country of Education:</strong> {composer.country_of_education.name}</p>
    <p><strong>Website:</strong> {composer.website}</p>
    <p><strong>Email:</strong> {composer.email}</p>
    <p><strong>More Info:</strong> {composer.more_info}</p>
    {composer.tags.map((tag) => (
      <span key={tag.tag_id}>{tag.name}</span>
    ))}
  </div>
}

