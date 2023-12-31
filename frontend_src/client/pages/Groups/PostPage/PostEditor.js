import React from 'react'
import classnames from 'classnames'
import request from 'superagent'
import { find } from 'lodash'

import ReactMde, { ReactMdeCommands, ReactMdeTextHelper } from 'react-mde'


class PostEditor extends React.Component {
    state = {
        editorVisible: false,
        reactMdeValue: { text: '' },
        previewVisible: false,
        editingPost: -1
    }

    componentDidUpdate = (prevProps, prevState) => {
        if (prevProps.editingPost !== this.props.editingPost & this.props.editingPost !== -1) {
            this.setState({
                editingPost: this.props.editingPost,
                reactMdeValue: {
                    text: find(this.props.posts, ['id', this.props.editingPost]).post
                },
                editorVisible: true
            })
        }
    }

    handleAddPostButtonClick = (e) => {
        this.setState(prevState => ({
            editorVisible: !prevState.editorVisible
        }))
    }

    handleMDEChange = (value) => {
        if (!value.text.length && this.state.editingPost !== -1) {
            this.setState({
                editingPost: -1
            }, () => this.props.updateEditingPost(-1))
        }
        this.setState({
            reactMdeValue: value
        })
    }

    togglePreview = (e) => {
        this.setState(prevState => ({
            previewVisible: !prevState.previewVisible
        }))
    }

    onImageInputChange = (e) => {
        if (e.target.files[0]) {
            const fileName = e.target.files[0].name
            request
                .post('/api/groups/posts/uploadimage/')
                .set('X-CSRFToken', window.django.csrf)
                .attach('image', e.target.files[0])
                .end((err, res) => {
                    if (res.ok) {
                        const {text, selection, scrollTop} = this.state.reactMdeValue
                        const {newText, insertionLength} = ReactMdeTextHelper.insertText(text, "![", selection.start)
                        const finalText = ReactMdeTextHelper.insertText(newText, `${fileName}](${res.body})`, selection.end + insertionLength).newText
                        this.setState({
                            reactMdeValue: {
                                text: finalText,
                                scrollTop,
                                selection
                            }
                        })
                    }
                })
        }
    }

    createOrUpdatePost = (e) => {
        const post = this.state.reactMdeValue.text
        if (post.length) {
            const {
                groupID,
                createPost,
                updatePost
            } = this.props
            if (this.state.editingPost !== -1) {
                const url = `/api/groups/posts/${this.state.editingPost}/`
                updatePost(url, post, groupID)
            } else {
                const url = '/api/groups/posts/'
                createPost(url, post, groupID)
            }
            this.setState({
                reactMdeValue:{
                    'text': ''
                },
                editorVisible: false,
                editingPost: -1
            }, () => this.props.updateEditingPost(-1))
        }
    }

    imageCommand = {
        icon: "image",
        tooltip: "Insert a picture",
        execute: (text, selection) => {
            $('#imageInput').click()
            return {
                text: text,
                selection: selection
            }
        }
    }

    render() {
        const  {
            className
        } = this.props

        const {
            editorVisible,
            previewVisible
        } = this.state

        const cx = classnames(className, 'ui-post-editor')

        let editorCommands = [ReactMdeCommands.getDefaultCommands()[0], ReactMdeCommands.getDefaultCommands()[1].slice(0, 3), ReactMdeCommands.getDefaultCommands()[2]]
        editorCommands.push([this.imageCommand])

        return (
            <div className={cx}>
                <div className={`editor-area ${editorVisible? 'visible': ''}`}>
                  <ReactMde
                    textAreaProps={{'placeholder': 'Type here'}}
                    value={this.state.reactMdeValue}
                    visibility={{preview: previewVisible, previewHelp: false, textarea: !previewVisible, toolbar: !previewVisible}}
                    onChange={this.handleMDEChange}
                    commands={editorCommands}
                    showdownOptions={{
                        simpleLineBreaks: true
                    }}
                    />
                    <div className='action-buttons'>
                        <button
                            className='preview-btn'
                            title={`${previewVisible ? 'hide preview': 'show preview'}`}
                            onClick={this.togglePreview}>
                                <i className={`fas ${previewVisible ? 'fa-eye-slash': 'fa-eye'}`}></i>
                        </button>
                        <button
                            className='post-btn'
                            title='post'
                            onClick={this.createOrUpdatePost}>
                                <i className='fas fa-paper-plane'></i>
                        </button>
                        <input type='file' accept='image/*' onChange={this.onImageInputChange} id='imageInput' style={{'visibility': 'hidden'}}/>
                    </div>
                </div>
                <button className={`add-post-btn ${editorVisible? 'editor-visible': ''}`} onClick={this.handleAddPostButtonClick}><i className='material-icons'>edit</i></button>
            </div>
        )
    }
}

export default PostEditor
