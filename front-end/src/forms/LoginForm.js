import React, { Component, useState } from "react";

const LoginForm = () => {
    const [state, setState] = React.useState({
        username: "",
        password: ""
    });

    function handleChange(event) {
      const value = event.target.value;
      setState({
        ...state,
        [event.target.name]: value
      });
    }

    function handleSubmit(event) {
        alert("E");
    }

    return (
        <div className="container">
            <div className="row">
                <div className="col-md-5 mx-auto">
                    <h1>Login</h1>
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="username">Username</label>
                            <input
                                type="username"
                                className="form-control"
                                name="username"
                                value={state.username}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input type="password"
                                   className="form-control"
                                   name="password"
                                   value={state.password}
                                   onChange={handleChange}
                            />
                        </div>
                        <div className="form-group form-check">
                            <input type="checkbox" className="form-check-input" id="exampleCheck1" />
                                <label className="form-check-label" htmlFor="exampleCheck1">Check me out</label>
                        </div>
                        <input type="submit" value="Submit" />
                    </form>
                </div>
            </div>
        </div>
    )
}

export default LoginForm;