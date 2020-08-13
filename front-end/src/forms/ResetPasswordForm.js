import React, { useState } from "react";
import axios from 'axios';
import { useHistory } from "react-router-dom";
import { useForm } from "react-hook-form";

const ResetPasswordForm = ({ match }) => {
    const { register, watch, handleSubmit, errors } = useForm();

    const params = match.params;

    const token = params.token;

    const onSubmit = resetUser => {
        return axios
            .post('/reset/password/' + token, {
                token: token,
                password: resetUser.password
            })
            .then(res => {
                console.log(res);
            })
            .catch((err) => {
                console.log(err);
            })
    }

    return (
        <div className="container">
            <div className="row">
                <div className="col-md-5 mx-auto">
                    <h1>Reset Password</h1>
                    <form autoComplete={`off`} onSubmit={handleSubmit(onSubmit)}>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input
                                type="password"
                                className="form-control"
                                name="password"
                                ref={register({ required: true, minLength: 4 })}
                            />
                            {errors.password && errors.password.type === "required" && (
                                <p>password is required</p>
                            )}
                            {errors.password && errors.password.type === "minLength" && (
                                <p>password is required min length of 4</p>
                            )}
                        </div>
                        <div className="form-group">
                            <label htmlFor="confirm">Confirm Password</label>
                            <input
                                type="password"
                                className="form-control"
                                name="confirm"
                                ref={register({
                                    required: true,
                                    minLength: 4,
                                    validate: (value) => {
                                        return value === watch('password');
                                    }
                                })}
                            />
                            {errors.confirm && errors.confirm.type === "required" && (
                                <p>confirm password is required</p>
                            )}
                            {errors.confirm && errors.confirm.type === "minLength" && (
                                <p>confirm password is required min length of 4</p>
                            )}
                            {errors.confirm && (
                                <p>The passwords do not match</p>
                            )}
                        </div>
                        <input type="submit" className={`btn btn-primary`} value={`Submit`} />
                    </form>
                </div>
            </div>
        </div>
)
}

export default ResetPasswordForm;