import React, {useEffect, useState} from 'react'
import axios from 'axios';

import SideBar from "../../includes/SideBar";


const SinglePostPage = (props) => {
    const [data, setData] = useState([{
        title: ''
    }]);

    useEffect(() => {
        const id = props.match.params.id;

        axios.get('/api/post/' + id)
            .then(res => {
                setData(res.data.data);
            })
            .catch(err => {
                console.log(err);
            });
    }, [data]);

    return (
        <React.Fragment>
            <div className="container-fluid">
                <div className="row">
                    <SideBar/>

                    <main role="main" className="col-md-9 ml-sm-auto col-lg-10 px-4">
                        <div
                            className="justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                            <input className="form-control form-control-lg" type="text" value={data.title} />
                            <br/>
                            <textarea className="form-control" id="post__content" rows={10} value={data.content} />
                        </div>

                    </main>
                </div>
            </div>
        </React.Fragment>
    )
}

export default SinglePostPage;