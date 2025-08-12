import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ComposerForm from './components/ComposerForm';

function ComposerEditPage() {
    const { composer_id } = useParams();
    const [composer, setComposer] = useState(null);
    const [loading, setLoading] = useState(true);

    async function fetchComposer() {
        const response = await fetch("http://localhost:8080/api/composers/" + composer_id);
        const data = await response.json();
        setComposer(data);
        setLoading(false)
    }

    useEffect(() => {
        fetchComposer();
    }, []);

    if (loading) {
        return <h1>Loading</h1>
    }

    return (
        <>
            <ComposerForm composer={composer} />
        </>
    );
}

export default ComposerEditPage
