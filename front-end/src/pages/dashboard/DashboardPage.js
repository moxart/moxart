import React from 'react'
import { Redirect } from 'react-router-dom';
import jwt_decode from 'jwt-decode'

import SideBar from "../../includes/SideBar";
import GetUsersComponents from "../../components/dashboard/GetUsersComponent";
import GetPostsComponents from "../../components/dashboard/GetPostsComponent";

const DashboardHomePage = () => {
    const state = {
        access_token: '',
        identity: ''
    };

    if (localStorage.getItem('access_token')) {
        state.access_token = localStorage.getItem('access_token');
        state.identity = jwt_decode(state.access_token);
    } else {
        return <Redirect to="/login" />
    }

    return (
        state.identity && <React.Fragment>
            <div className="container-fluid">
                <div className="row">
                    <SideBar/>

                    <main role="main" className="col-md-9 ml-sm-auto col-lg-10 px-4">
                        <div
                            className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                            <h1 className="h2">Dashboard</h1>
                        </div>

                        <GetPostsComponents/>
                        <GetUsersComponents/>
                    </main>
                </div>
            </div>
        </React.Fragment>
    )
};

export default DashboardHomePage;