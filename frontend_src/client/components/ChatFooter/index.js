import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import { Picker }  from 'emoji-mart'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './ChatFooter.styl'

class ChatFooter extends Component {
	constructor(props) {
		super(props)
		this.state = {
			emojiButtonClicked: false,
			chatMessage: '',
			lastTypingSynchedOn: new Date(0),
			syncDelayInMillis: 5000,
			chatAttachment: null,
			imageLoaded: false,
			fileLoaded: false,
			inputPlaceholder: 'Type here or click on attachment buttons'
		}
	}

	onEmojiButtonClick = () => {
		if (!this.state.emojiButtonClicked) {
			document.addEventListener('click', this.handleClickOutside, false)
		} else {
			document.removeEventListener('click', this.handleClickOutside, false)
		}
		this.setState(prevState => ({
			emojiButtonClicked: !prevState.emojiButtonClicked
		}))
	}

	handleClickOutside = (e) => {
		if (this.emojinode.contains(e.target)) {
			return
		}
		this.onEmojiButtonClick()
	}

	onEmojiClick = (emoji, event) => {
		this.setState(prevState => ({
			chatMessage: prevState.chatMessage + ` ${emoji.colons} `
		}))
	}

	onChatSend = (e)=> {
		const msg = e.target.value;
		if (new Date().getTime() - this.state.lastTypingSynchedOn.getTime() > this.state.syncDelayInMillis) {
			if (this.props.roomId) {
				this.props.handleTypingStatus(this.props.roomId)
			} else {
				this.props.handleTypingStatus()
			}
			this.setState({
				lastTypingSynchedOn: new Date()
			})
		}
		this.setState({
			chatMessage: msg
		})
	}

	handleSendChat = (e) => {
		e.preventDefault()
		if (this.state.chatMessage || this.state.chatAttachment) {
			if (this.state.chatAttachment) {
				if (this.props.roomId) {
					this.props.handleSendChat(this.props.roomId, this.state.chatMessage, this.state.chatAttachment)	
				} else {
					this.props.handleSendChat(this.state.chatMessage, this.state.chatAttachment)
				}
				$('#fileInput')[0].value = null
				$('#imageInput')[0].value = null
			} else {
				if (this.props.roomId) {
					this.props.handleSendChat(this.props.roomId, this.state.chatMessage)	
				} else {
					this.props.handleSendChat(this.state.chatMessage)
				}
			}
			this.setState({
				chatMessage: '',
				chatAttachment: null,
				imageLoaded: false,
				fileLoaded: false,
				inputPlaceholder: 'Type here or click on attachment buttons'
			})	
		}
	}

	onImageButtonClick = (e) => {
		e.preventDefault()
		$('#imageInput').click()
	}

	onFileButtonClick = (e) => {
		e.preventDefault()
		$('#fileInput').click()
	}

	handleInputChange = (e, inputtype) => {
		if (e.target.files[0]) {
			if (inputtype === 'image') {
				$('#fileInput')[0].value = null
				this.setState({
					chatAttachment: e.target.files[0],
					imageLoaded: true,
					fileLoaded: false,
					inputPlaceholder: "Nice! now you can add a caption here or send by pressing enter here"
				})
			} else {
				$('#imageInput')[0].value = null
				this.setState({
					chatAttachment: e.target.files[0],
					fileLoaded: true,
					imageLoaded: false,
					inputPlaceholder: "Nice! now you can add a caption here or send by pressing enter here"
				})
			}
		} else {
			this.setState({
				fileLoaded: false,
				imageLoaded: false,
				chatAttachment: null,
				inputPlaceholder: 'Type here or click on attachment buttons'
			})
		}
	}

	render(){
		const {
			className,
			small = false,
			onChatInputFocus = () => null
		} = this.props;

		const cx = classnames(
			c.container, className, 'chatview-footer ui-chat-footer flex-horizontal a-stretch',{
				'is-small': small
			}
		)

		return (
			<div className={cx}>
				<div className='btn btn-default ui-button btn-attachment' onClick={this.onFileButtonClick}>
					<i className={classnames('fa fa-paperclip', {'file-load-indicator': this.state.fileLoaded})}/>
				</div>
				<div className='btn btn-default ui-button btn-camera' onClick={this.onImageButtonClick}>
					<i className={classnames('fa fa-camera-retro', { 'file-load-indicator': this.state.imageLoaded })} />
				</div>
				<div className='chat-input-wrap flex-1 flex-horizontal a-stretch'>
					{this.props.showTyping && <div className="chat-user-typing">
						<span>{this.props.showTypingUsername || "User"} is typing <i className="fa fa-spin fa-circle-o-notch"></i></span>
					</div>}
					<form onSubmit={this.handleSendChat}>
						<input
							className='chat-input-box'
							type='text'
							placeholder={this.state.inputPlaceholder}
							spellCheck={true}
							value={this.state.chatMessage}
							onInput={this.onChatSend}
							onFocus={onChatInputFocus} />
						<input
							type='file'
							id="imageInput"
							accept='.png, .gif, .jpg, .mp4, .avi'
							style={{'display': 'none'}}
							onChange={(e) => this.handleInputChange(e, 'image')} />
						<input
							type='file'
							id="fileInput"
							style={{ 'display': 'none' }}
							onChange={(e) => this.handleInputChange(e, 'file')} />
						<div className="file-upload-bar" style={{'width': this.props.uploadProgress + '%'}}></div>
						<div className='btn btn-default ui-button chat-input-btn' onClick={this.handleSendChat}>
							<i className='fa fa-paper-plane'/>
						</div>
					</form>
				</div>
				<div className="emoji-wrapper" ref={node => {this.emojinode = node}} style={{position: 'relative', zIndex: 9999}}>
					{this.state.emojiButtonClicked && <Picker
						title='Pick your emoji…'
						emoji='point_up'
						style={{ position: 'absolute', bottom: '55px', right: '20px', width: '300px' }}
						showPreview={false}
						emojiSize={20}
						onClick={this.onEmojiClick} />}
					<div className='btn btn-default ui-button' onClick={this.onEmojiButtonClick}>
						<i className='fa fa-smile-o' />
					</div>
				</div>
			</div>
		)
	}
}

export default withStyles(c)(ChatFooter)
