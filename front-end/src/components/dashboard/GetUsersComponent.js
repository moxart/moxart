import React, {useState, useEffect} from 'react';
import axios from 'axios';

const GetUsersComponents = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.post('/api/users')
            .then(res => {
                setData(res.data);
            })
            .catch(err => {
                console.log(err);
            })
    }, [data]);

    const removeData = (user) => {

        axios.delete('/api/user/' + user)
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
            <h3><span className="badge badge-secondary">Users</span></h3>
            <div className="table-responsive dashboard__users">
                <table className="table table-striped table-md">
                    <thead>
                    <tr>
                        <th/>
                        <th>public id</th>
                        <th>username</th>
                        <th>email</th>
                        <th>admin</th>
                        <th>last activity</th>
                        <th>registered at</th>
                        <th>confirmed</th>
                        <th>confirmed at</th>
                        <th/>
                    </tr>
                    </thead>
                    <tbody>
                    {data.map((user, index) => (
                        <tr key={index++}>
                            <td>{index}</td>
                            <td>{user.user_public_id}</td>
                            <td>{user.username}</td>
                            <td>{user.email}</td>
                            <td>
                                <h6
                                    dangerouslySetInnerHTML={{__html: user.admin ? "<span class=\"badge badge-success\">Yes</span>" : "<span class=\"badge badge-danger\">No</span>"}}/>
                            </td>
                            <td>{user.last_activity}</td>
                            <td>{user.registered_at}</td>
                            <td>
                                <h6
                                    dangerouslySetInnerHTML={{__html: user.confirmed ? "<span class=\"badge badge-success\">Yes</span>" : "<span class=\"badge badge-warning\">No</span>"}}/>
                            </td>
                            <td>{user.confirmed_at}</td>
                            <td>
                                <button onClick={() => removeData(user.username)}
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

export default GetUsersComponents;