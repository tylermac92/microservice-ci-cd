import React, { useEffect, useState } from 'react';

function App() {
    const [health, setHealth] = useState(null);

    useEffect(() => {
        fetch(process.env.REACT_APP_BACKEND_URL + "/health")
            .then(res => res.json())
            .then(setHealth)
            .catch(err => console.error("Health check failed", err));
    }, []);

    return (
        <div>
            <h1>Microservice Frontend</h1>
            <p>Status: {health ? health.status : "Loading..."}</p>
        </div>
    );
}

export default App;
