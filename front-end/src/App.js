import React from 'react'
import { BrowserRouter as Router, Route } from "react-router-dom";

import NavBar from "./includes/NavBar";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ResetPasswordForm from "./forms/ResetPasswordForm";
import UploadFileForm from "./forms/UploadFileForm";

function App() {
  return (
    <Router>
        <div className="App">
            <NavBar />
            <div id="app-body">
                <Route path={`/`} component={HomePage} exact />
                <Route path={`/about`} component={AboutPage} />
                <Route path={`/contact`} component={ContactPage} />
                <Route path={`/register`} component={RegisterPage} />
                <Route path={`/login`} component={LoginPage} />
                <Route path={`/reset/password/:token`} component={ResetPasswordForm} />
                <Route path={`/upload`} component={UploadFileForm} />
            </div>
        </div>
    </Router>
  );
}

export default App;
