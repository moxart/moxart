import React, { useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";
import {useHistory} from "react-router-dom";

const RegisterForm = () => {
    const history = useHistory();

    const { register, handleSubmit, errors } = useForm();

    const onSubmit = RegisterUser => {
        return axios
            .post('/register', {
                username: RegisterUser.username,
                email: RegisterUser.email,
                password: RegisterUser.password
            })
            .then(res => {
                localStorage.setItem('access_token', res.data.access_token);
                // return res.data;
                history.push('/login');
            })
            .catch(err => {
                console.log(err);
            });
    }


    return (
        <div className="container">
            <div className="row">
                <div className="col-md-5 mx-auto">
                    <h1>Register</h1>

                    <form autoComplete={`off`} onSubmit={handleSubmit(onSubmit)}>
                        <div className="form-group">
                            <label htmlFor="username">Username</label>
                            <input
                                type="username"
                                className="form-control"
                                name="username"
                                ref={register({ required: true, minLength: 4 })}
                            />
                            {errors.username && errors.username.type === "required" && (
                                <p>username is required</p>
                            )}
                            {errors.username && errors.username.type === "minLength" && (
                                <p>username is required min length of 4</p>
                            )}
                        </div>
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                type="email"
                                className="form-control"
                                name="email"
                                ref={register({ required: true })}
                            />
                            {errors.email && errors.email.type === "required" && (
                                <p>email is required</p>
                            )}
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input type="password"
                                   className="form-control"
                                   name="password"
                                   ref={register({ required: true, minLength: 6 })}
                            />
                            {errors.password && errors.password.type === "required" && (
                                <p>password is required</p>
                            )}
                            {errors.password && errors.password.type === "minLength" && (
                                <p>password is required min length of 6</p>
                            )}
                        </div>

                        <input type="submit" className={`btn btn-primary`} value={`Register`} />
                    </form>
                </div>
            </div>
        </div>
    )
}

export default RegisterForm;
