import React from 'react'
import Dropzone from 'react-dropzone'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './DropzoneWrapper.styl'


class DropzoneWrapper extends React.Component {
    render() {
        const {
            files,
            accept=".png, .jpg",
            label="Drop attachments here",
            onDrop,
            onTrashClick
        } = this.props

        return (
            <Dropzone onDrop={onDrop} className={c.container} accept={accept}>
                <p style={{ margin: 0 }}>{label}</p>
                <div className="dropped-files">
                    <ul>
                        {
                            files &&
                            files.map(
                                (f, i) =>
                                    <li key={i}>
                                        <i className="fa fa-paperclip"></i> {f.name}
                                        <i className="fa fa-trash remove-file" onClick={(e) => onTrashClick(e, f.name)}></i>
                                    </li>
                            )
                        }
                    </ul>
                </div>
            </Dropzone>
        )
    }
}

export default withStyles(c)(DropzoneWrapper)
