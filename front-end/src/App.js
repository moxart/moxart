import React from 'react'
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";

import NavBar from "./includes/NavBar";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ResetPasswordForm from "./forms/ResetPasswordForm";
import UploadFileForm from "./forms/UploadFileForm";
import PostsPage from "./pages/dashboard/PostsPage";
import SinglePostPage from "./pages/dashboard/SinglePostPage";
import NewPostPage from "./pages/dashboard/NewPostPage";
import DashboardHomePage from "./pages/dashboard/DashboardPage";

function App() {
    return (
        <Router>
            <div className="App">
                <NavBar/>
                <div id="app-body">
                    <Switch>
                        <Route path={`/dashboard/home`} component={DashboardHomePage} exact/>
                        <Route path={`/dashboard/posts`} component={PostsPage}/>
                        <Route path={`/dashboard/post/:id`} component={SinglePostPage}/>
                        <Route path={`/dashboard/new/post`} component={NewPostPage}/>

                        <Route path={`/about`} component={AboutPage}/>
                        <Route path={`/contact`} component={ContactPage}/>
                        <Route path={`/register`} component={RegisterPage}/>
                        <Route path={`/login`} component={LoginPage}/>
                        <Route path={`/reset/password/:token`} component={ResetPasswordForm}/>
                        <Route path={`/upload`} component={UploadFileForm}/>
                    </Switch>

                </div>
            </div>
        </Router>
    );
}

export default App;
