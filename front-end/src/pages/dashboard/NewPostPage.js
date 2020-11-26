import React from 'react'
import {useForm} from "react-hook-form";
import axios from 'axios';
import {Editor} from '@tinymce/tinymce-react';
import {useHistory} from "react-router-dom";

import SideBar from "../../includes/SideBar";

const NewPostPage = () => {
    const history = useHistory();

    const {register, handleSubmit, errors} = useForm();

    const state = {
        post: {
            content: ''
        }
    }

    const handleEditorChange = (content, editor) => {
        state.post.content = content;
    }

    const onSubmit = RegisterPost => {
        return axios
            .post('/api/post', {
                user_public_id: '9aac053c-f048-49f0-8734-1bcf2ec9a278',
                category_public_id: 'a82b03a5-ac67-4ab1-a940-f94250a8fd41',
                title: RegisterPost.title,
                content: state.post.content
            })
            .then(res => {

                history.push('/dashboard/posts');

            })
            .catch(err => {
                console.log(err);
            });
    }

    return (
        <React.Fragment>
            <div className="container-fluid">
                <div className="row">
                    <SideBar/>

                    <main role="main" className="col-md-9 ml-sm-auto col-lg-10 px-4">
                        <div
                            className="justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                            <form autoComplete="off" onSubmit={handleSubmit(onSubmit)}>
                                <input type="text" name="title" id="title" className="form-control form-control-lg"
                                       placeholder="Title"
                                       ref={register({required: true, maxLength: 30})} />
                                {errors.title && errors.title.type === "required" && (
                                    <p>title is required</p>
                                )}
                                {errors.title && errors.title.type === "minLength" && (
                                    <p>title is required min length of 4</p>
                                )}
                                <br/>

                                <Editor
                                    initialValue="<p>This is the initial content of the editor</p>"
                                    ref={register({required: true})}
                                    name="content"
                                    init={{
                                        height: 500,
                                        menubar: false,
                                        plugins: [
                                            'advlist autolink lists link image charmap print preview anchor',
                                            'searchreplace visualblocks code fullscreen',
                                            'insertdatetime media table paste code help wordcount'
                                        ],
                                        toolbar:
                                            'undo redo | formatselect | bold italic backcolor | \
                                            alignleft aligncenter alignright alignjustify | \
                                            bullist numlist outdent indent | removeformat | help'
                                    }}
                                    onEditorChange={handleEditorChange}
                                />

                                <br/>
                                <input type="submit" className={`btn btn-secondary`} value={`Publish`}/>
                            </form>
                        </div>

                    </main>
                </div>
            </div>
        </React.Fragment>
    )
}

export default NewPostPage;