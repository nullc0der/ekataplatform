import React from 'react'
import classnames from 'classnames'
import { connect } from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'

import { actions } from 'store/Common'
import Modal from 'components/ui/Modal'
import Slider from 'components/ui/Slider'
import s from './ImageEditor.styl'


class ImageEditor extends React.Component {
    state = {
        slider: {
            rotate: 0,
            zoom: 1.00,
            brightness: 0,
            hue: 0
        },
        caption: '',
        filename: '',
        canvasShown: true,
        loadButtonsShown: true,
        videoButtonsShown: false,
        imageButtonsShown: false
    }

    onCaptionChange = (e) => {
        e.preventDefault()
        this.setState({
            caption: e.target.value
        })
    }

    onSliderChange = (e) => {
        e.preventDefault()
        const isCanvasBlank = this.isCanvasBlank(this.canvasEl)
        const slider = this.state.slider
        slider[e.target.name] = e.target.value
        this.setState({
            slider: slider
        })
        switch(e.target.name) {
            case 'zoom':
                if (!isCanvasBlank) {
                    this.canvasEl.removeAttribute('data-caman-id')
                    this.zoom(this.state.slider['zoom'], -this.state.slider['rotate'])
                }
            case 'rotate':
                if (!isCanvasBlank) {
                    this.canvasEl.removeAttribute('data-caman-id')
                    this.rotate(-this.state.slider['rotate'], this.state.slider['zoom'])
                }
            case 'brightness':
                if (!isCanvasBlank && this.state.slider['brightness'] != 0) {
                    const brightness = this.state.slider['brightness']
                    const hue = this.state.slider['hue']
                    Caman(
                        this.canvasEl,
                        function () {
                            this.revert(false)
                            this
                                .brightness(parseInt(brightness))
                                .hue(parseInt(hue))
                                .render()
                        }
                    )
                }
            case 'hue':
                if (!isCanvasBlank && this.state.slider['hue'] != 0) {
                    const brightness = this.state.slider['brightness']
                    const hue = this.state.slider['hue']
                    Caman(
                        this.canvasEl,
                        function () {
                            this.revert(false)
                            this
                                .hue(parseInt(hue))
                                .brightness(parseInt(brightness))
                                .render()
                        }
                    )
                }
        }
    }

    onImageButtonClick = (e) => {
        e.preventDefault()
        this.imageInput.click()
    }

    onVideoButtonClick = (e) => {
        e.preventDefault()
        this.setState({
            canvasShown: false,
            loadButtonsShown: false,
            videoButtonsShown: true
        })
        this.initiateVideo()
    }

    onResetButtonClick = (e) => {
        e.preventDefault()
        const ctx = this.canvasEl.getContext('2d')
        ctx.clearRect(0, 0, this.canvasEl.width, this.canvasEl.height)
        this.setState({
            loadButtonsShown: true,
            imageButtonsShown: false
        })
        this.resetSliders()
    }

    onFileInputChange = (e) => {
        e.preventDefault()
        if (e.target.files[0]) {
            this.buildImageFromFile(e.target.files)
            this.setState({
                loadButtonsShown: false,
                imageButtonsShown: true
            })
        }
    }

    resetSliders = () => {
        this.canvasEl.removeAttribute('data-caman-id')
        this.setState({
            slider: {
                rotate: 0,
                zoom: 1.00,
                brightness: 0,
                hue: 0
            }
        })
    }

    setVideoSource = (stream) => {
        this.videoEl.src = URL.createObjectURL(stream)
        this.lstream = stream
    }

    initiateVideo = () => {
        const addNotification = this.props.addNotification
        const setVideoSource = this.setVideoSource
        navigator.getUserMedia = navigator.webkitGetUserMedia ||	// WebKit
            navigator.mozGetUserMedia ||	// Mozilla FireFox
            navigator.getUserMedia			// 2013...
        if (!navigator.getUserMedia) {
            addNotification({
                message: 'Sorry, Your browser doesn\'t supports this function',
                level: 'error'
            })
        }
        navigator.getUserMedia({
                audio: false,
                video: true
            },
            stream => setVideoSource(stream),
            err => addNotification({
                message: 'No video source detected! Please allow camera access',
                level: 'error'
            })
        )
    }

    stopVideo = (e) => {
        this.setState({
            canvasShown: true,
            loadButtonsShown: true,
            videoButtonsShown: false
        })
        this.videoEl.pause()
        this.videoEl.src = ""
        this.lstream.getTracks()[0].stop()
    }

    takeVideo = (e) => {
        const live = this.videoEl
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext("2d")
        canvas.width = live.clientWidth
        canvas.height = live.clientHeight
        ctx.drawImage(live, 0, 0, canvas.width, canvas.height)
        this.updateCanvas(canvas.toDataURL('image/png'))
        this.stopVideo()
        this.setState({
            canvasShown: true,
            loadButtonsShown: false,
            videoButtonsShown: false,
            imageButtonsShown: true,
            filename: 'webcam.png'
        })
    }

    updateCanvas = (datasrc) => {
        this.img = new Image()
        const img = this.img
        img.src = datasrc
        img.onload = () => {
            this.canvasEl.removeAttribute('data-caman-id')
            const ctx = this.canvasEl.getContext('2d')
            ctx.clearRect(0, 0, this.canvasEl.width, this.canvasEl.height)
            ctx.drawImage(
                img,
                0, 0, img.width, img.height,
                0, 0, this.canvasEl.width, this.canvasEl.height
            )
        }
    }

    buildImageFromFile = (files) => {
        if (files && files.length) {
            const file = files[0]
            const reader = new FileReader()
            reader.onload = e => this.updateCanvas(e.target.result)
            reader.readAsDataURL(file)
            this.setState({
                filename: file.name
            })
        }
    }

    isCanvasBlank = (canvas) => {
        const blank = document.createElement('canvas')
        blank.height = canvas.height
        blank.width = canvas.width

        return canvas.toDataURL() == blank.toDataURL()
    }

    zoom = (scale, degrees, cx=this.canvasEl.width/2, cy=this.canvasEl.height/2) => {
        const ctx = this.canvasEl.getContext('2d')
        ctx.clearRect(0, 0, this.canvasEl.width, this.canvasEl.height)
        ctx.save()
        ctx.translate(cx, cy)
        if (degrees) {
            ctx.rotate(degrees*Math.PI/180)
        }
        ctx.scale(scale, scale)
        ctx.drawImage(this.img, -this.img.width / 2, -this.img.height / 2)
        ctx.restore()
    }

    rotate = (degrees, scale, cx = this.canvasEl.width / 2, cy = this.canvasEl.height / 2) => {
        const ctx = this.canvasEl.getContext('2d')
        ctx.clearRect(0, 0, this.canvasEl.width, this.canvasEl.height)
        ctx.save()
        ctx.translate(cx, cy)
        if (scale) {
            ctx.scale(scale, scale)
        }
        ctx.rotate(degrees * Math.PI / 180)
        ctx.drawImage(this.img, -this.img.width/2, -this.img.height/2)
        ctx.restore()
    }

    onUploadButtonClick = (e) => {
        if(!this.isCanvasBlank(this.canvasEl)) {
            this.canvasEl.toBlob(blob => {
                blob.name = this.state.filename
                this.props.uploadImage(blob, this.state.caption)
            })
            this.onResetButtonClick(e)
        } else {
            this.props.addNotification({
                message: "No blank upload is allowed",
                level: "warning"
            })
        }
    }


    render() {
        const {
            className,
            isOpen,
            onBackdropClick,
            showCaption=false
        } = this.props

        const extraClass = $(window).width() < 768 ? 'flex-vertical a-center' : 'flex-horizontal a-stretch'

        const cx = classnames(
            s.container, className, extraClass
        )

        const footerChildren = (
            <button className="btn btn-default" onClick={this.onUploadButtonClick}>Upload</button>
        )

        return (
            <Modal
                id="image-editor-modal"
                isOpen={isOpen}
                title="Upload image"
                onBackdropClick={onBackdropClick}
                footer={true}
                footerChildren={footerChildren}>
                <div className={cx}>
                    <div className="image-wrapper">
                        <div className={classnames("load-image-buttons", { 'hide': !this.state.loadButtonsShown })}>
                            <button className="btn-rounded" onClick={this.onImageButtonClick}><i className="fa fa-file-image-o"></i></button>
                            <button className="btn-rounded" onClick={this.onVideoButtonClick}><i className="fa fa-camera-retro"></i></button>
                        </div>
                        <div className={classnames("video-actions", {'hide': !this.state.videoButtonsShown})}>
                            <button className="btn-rounded" onClick={this.stopVideo}><i className="fa fa-times-circle"></i></button>
                            <button className="btn-rounded" onClick={this.takeVideo}><i className="fa fa-check-circle"></i></button>
                        </div>
                        <div className={classnames("image-actions", {"hide": !this.state.imageButtonsShown})}>
                            <button className="btn-rounded" onClick={this.onResetButtonClick}><i className="fa fa-times-circle"></i></button>
                        </div>
                        <canvas ref={node => this.canvasEl = node} width={300} height={300}
                            className={classnames('image', {'hide': !this.state.canvasShown})} />
                        <video ref={node => this.videoEl = node} width={300} height={300}
                            className={classnames('video', { 'hide': this.state.canvasShown })} />
                        <input 
                            type="file" accept="image/*" style={{'display': 'none'}}
                            ref={node => this.imageInput = node} onChange={this.onFileInputChange} />
                    </div>
                    <div className="editor-options">
                        <div className="editor-option-rotate">
                            <p className="editor-info"><i className="fa fa-refresh"></i> Rotate</p>
                            <Slider name="rotate" value={this.state.slider["rotate"]} min="-180" max="180" onChange={this.onSliderChange} />
                        </div>
                        <div className="editor-option-zoom">
                            <p className="editor-info"><i className="fa fa-arrows-alt"></i> Zoom</p>
                            <Slider name="zoom" value={this.state.slider["zoom"]} min="0.5" max="1.5" step="0.10" onChange={this.onSliderChange} />
                        </div>
                        <div className="editor-option-brightness">
                            <p className="editor-info"><i className="fa fa-certificate"></i> Brightness</p>
                            <Slider name="brightness" value={this.state.slider["brightness"]} min="-100" max="100" onChange={this.onSliderChange} />
                        </div>
                        <div className="editor-option-hue">
                            <p className="editor-info"><i className="fa fa-connectdevelop"></i> Hue</p>
                            <Slider name="hue" value={this.state.slider["hue"]} min="0" max="100" onChange={this.onSliderChange} /> 
                        </div>
                        {showCaption && <div className="editor-option-caption">
                            <p className="editor-info"><i className="fa fa-edit"></i> Caption</p>
                            <input className="form-control" id="inputCaption" type="text"
                                name="caption" value={this.state.caption} onChange={this.onCaptionChange} />
                        </div>}
                    </div>
                </div>
            </Modal>
        )
    }
}

const mapStateToProps = (state) => ({
})

const mapDispatchToProps = (dispatch) => ({
    addNotification: (notification) => dispatch(actions.addNotification(notification))
})

export default withStyles(s)(
    connect(mapStateToProps, mapDispatchToProps)(ImageEditor)
)
