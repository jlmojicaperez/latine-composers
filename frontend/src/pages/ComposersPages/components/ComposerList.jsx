import { useEffect, useState } from "react"
import { Link } from "react-router-dom"

export default function ComposerList({ composers }) {

  return <div>
    <h2> Composers </h2>
    <table>
      <thead>
        <tr>
          <th>Image</th>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {composers.map((composer) => (
          <tr key={composer.composer_id}>
            <td><img src={`http://localhost:8080/api/images/${composer.image.image_id}`} style={{ height: "128px" }} /></td>
            <td><Link to={`/composers/${composer.composer_id}`} >{composer.first_name} {composer.last_name}</Link></td>
            <td>
              <button onClick={() => update_composer(composer.composer_id)}>Update</button>
              <button onClick={() => delete_composer(composer.composer_id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
}

