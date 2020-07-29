import React, {useState, useEffect} from 'react'

const HomePage = () => {
    const [posts, setPosts] = useState({});

    useEffect(() => {
        const fetchData = async () => {

        }
        fetchData();
    }, []);

    return (
        <React.Fragment>
            <h1>Homepage</h1>
            <h3>Post: {posts.title}</h3>
        </React.Fragment>
    )
};

export default HomePage;