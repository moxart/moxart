import React from 'react';

const SideBar = () => {
    return (
        <React.Fragment>
            <nav className="col-md-2 d-none d-md-block bg-light sidebar">
                <div className="sidebar-sticky">
                    <ul className="nav flex-column">
                        <li className="nav-item">
                            <a className="nav-link active" href="/dashboard/home">
                                Dashboard <span className="sr-only">(current)</span>
                            </a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="/dashboard/home">
                                Home
                            </a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="/dashboard/posts">
                                Posts
                            </a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="/dashboard/new/post">
                                New Post
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </React.Fragment>
    )
};

export default SideBar;