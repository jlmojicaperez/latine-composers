import { useState, useEffect } from 'react';

export default function TagsSearchField({ addTag }) {
  const [tags, setTags] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  async function fetchTags() {
    const response = await fetch("http://localhost:8080/api/tags");
    const data = await response.json();
    setTags(data);
    setLoading(false)
  }

  function updatesearch(chars) {
    for (let index = 0; index < tags.length; index++) {
    }
  }

  useEffect(() => {
    fetchTags();
  }, []);

  if (loading) {
    return <h1>Loading</h1>
  }

  return (
    <>
      <input type='text' placeholder='Search tags...' onChange={(event) => setSearch(event.target.value)} value={search} />
      <div>
        <ul>
          {tags.filter((tag) => {
            if (search) {
              return tag.name.toLowerCase().includes(search.toLowerCase())
            }
            return true
          }).map((tag) => (
            <li key={tag.tag_id} onClick={() => { addTag(tag) }}><button type="button">{tag.name}</button></li>
          ))}
        </ ul>
      </div>
    </>
  );
}
