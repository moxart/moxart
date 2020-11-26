import React from 'react'
import SideBar from "../../includes/SideBar";
import GetPostsComponents from "../../components/dashboard/GetPostsComponent";


const PostsPage = () => {
    return (
        <React.Fragment>
            <div className="container-fluid">
                <div className="row">
                    <SideBar />

                    <main role="main" className="col-md-9 ml-sm-auto col-lg-10 px-4">
                        <div
                            className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                            <h1 className="h2">Posts</h1>
                        </div>

                        <GetPostsComponents />
                    </main>
                </div>
            </div>
        </React.Fragment>
    )
};

export default PostsPage;