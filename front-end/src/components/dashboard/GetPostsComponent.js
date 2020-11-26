import React, {useState, useEffect} from 'react';
import axios from 'axios';

const GetPostsComponents = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('/api/posts')
            .then(res => {
                setData(res.data);
            })
            .catch(err => {
                console.log(err);
            })
    }, [data]);

    const removeData = (user) => {

        axios.delete('/api/post/' + user)
            .then(res => {
                console.log(res);
                console.log(res.data);
            })
            .catch(err => {
                console.log(err)
            });
    }

    return (
        <React.Fragment>
            <h3><span className="badge badge-secondary">Latest Posts</span></h3>
            <div className="table-responsive dashboard__posts">
                <table className="table table-striped table-md">
                    <thead>
                    <tr>
                        <th/>
                        <th>title</th>
                        <th>comments</th>
                        <th>published at</th>
                        <th>updated at</th>
                        <th />
                        <th />
                        <th />
                    </tr>
                    </thead>
                    <tbody>
                    {data.map((post, index) => (
                        <tr key={index++}>
                            <td>{index}</td>
                            <td className="post__title"><a href={`/dashboard/post/${post.post_public_id}`}>{post.title}</a></td>
                            <td>{post.comment_count}</td>
                            <td>{post.published_at}</td>
                            <td>{post.updated_at}</td>
                            <td>{post.last_activity}</td>
                            <td>{post.registered_at}</td>
                            <td>
                                <button onClick={() => removeData(post.post_public_id)}
                                        className="btn btn-danger btn-sm __delete">Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </React.Fragment>
    );
}

export default GetPostsComponents;