import React from 'react';
import {Link, withRouter} from 'react-router-dom';
import {useHistory} from "react-router-dom";

const NavBar = () => {
    const history = useHistory();

    const handleLogout = history => () => {
        localStorage.removeItem("access_token");
        history.push('/login');
    }

    return (
        <React.Fragment>
            <nav className="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
                <a className="navbar-brand col-sm-3 col-md-2 mr-0" href="/dashboard/home">MOXART</a>
                <input className="form-control form-control-dark w-100" type="text" placeholder="Search"
                       aria-label="Search"/>
                <ul className="navbar-nav px-3">
                    <li className="nav-item text-nowrap">
                        <a className="nav-link" onClick={handleLogout(history)}>Sign out</a>
                    </li>
                </ul>
            </nav>
        </React.Fragment>
    );
}

export default NavBar;