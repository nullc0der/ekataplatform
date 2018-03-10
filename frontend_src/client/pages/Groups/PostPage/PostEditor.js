import React from 'react'
import classnames from 'classnames'

import ReactMde, {ReactMdeCommands} from 'react-mde'


class PostEditor extends React.Component {
    state = {
        editorVisible: false,
        reactMdeValue: { text: '' },
        previewVisible: false
    }

    handleAddPostButtonClick = (e) => {
        this.setState(prevState => ({
            editorVisible: !prevState.editorVisible
        }))
    }

    handleMDEChange = (value) => {
        this.setState({
            reactMdeValue: value
        })
    }

    togglePreview = (e) => {
        this.setState(prevState => ({
            previewVisible: !prevState.previewVisible
        }))
    }

    render() {
        const  {
            className,
            onClickSend
        } = this.props

        const {
            editorVisible,
            previewVisible
        } = this.state

        const cx = classnames(className, 'ui-post-editor')

        const editorCommands = [ReactMdeCommands.getDefaultCommands()[0], ReactMdeCommands.getDefaultCommands()[1].slice(0, 3), ReactMdeCommands.getDefaultCommands()[2]]

        return (
            <div className={cx}>
                <div className={`editor-area ${editorVisible? 'visible': ''}`}>
                  <ReactMde
                    value={this.state.reactMdeValue}
                    visibility={{preview: previewVisible, previewHelp: false, textarea: !previewVisible, toolbar: !previewVisible}}
                    onChange={this.handleMDEChange}
                    commands={editorCommands}
                    />
                    <div className='action-buttons'>
                        <button className='preview-btn' title='preview' onClick={this.togglePreview}><i className='fas fa-eye'></i></button>
                        <button className='post-btn' title='post' onClick={(e) => onClickSend(e, this.state.reactMdeValue.text)}><i className='fas fa-paper-plane'></i></button>
                    </div>
                </div>
                <button className={`add-post-btn ${editorVisible? 'editor-visible': ''}`} onClick={this.handleAddPostButtonClick}><i className='material-icons'>add</i></button>
            </div>
        )
    }
}

export default PostEditor
