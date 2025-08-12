import { useState, useEffect } from 'react'
import ComposerList from "./components/ComposerList";

function ComposersListPage() {
    const [composers, setComposers] = useState([]);

    async function fetchComposers() {
        const response = await fetch("http://localhost:8080/api/composers");
        console.log("Response: " + response)
        const data = await response.json();
        setComposers(data);
    }

    useEffect(() => {
        fetchComposers()
    }, [])

    if (composers.length === 0) {
        return <h1>No composers here :( </h1>

    }

    return (
        <>
            <ComposerList composers={composers} />
        </>
    );
}

export default ComposersListPage
