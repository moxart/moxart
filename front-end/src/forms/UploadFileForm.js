import React from 'react';
import { useForm } from "react-hook-form";
import axios from "axios";

const UploadFileForm = () => {
    const { register, handleSubmit } = useForm();

    const onSubmit = (data) => {
        console.log(data.file[0]);
        return axios
            .post('/upload', data, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(res => {
                console.log(res);
            })
            .catch(err => console.log(err));
    }

    return (
        <div className="container">
            <div className="row">
                <div className="col-md-5 mx-auto">
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <div className="form-group">
                            <label htmlFor="file">Upload File</label>
                            <input type="file"
                                   name="file"
                                   ref={register}
                            />
                        </div>
                        <input required type="submit" className={`btn btn-primary`} value={`Submit`} />
                    </form>
                </div>
            </div>
        </div>
    )
}

export default UploadFileForm;