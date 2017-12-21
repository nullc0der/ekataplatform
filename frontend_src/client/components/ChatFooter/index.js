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
			syncDelayInMillis: 5000
		}
		this.onEmojiButtonClick = this.onEmojiButtonClick.bind(this)
	}

	onEmojiButtonClick = () => {
		this.setState(prevState => ({
			emojiButtonClicked: !prevState.emojiButtonClicked
		}))
	}

	onEmojiClick = (emoji, event) => {
		this.setState(prevState => ({
			chatMessage: prevState.chatMessage + ` ${emoji.colons} `
		}))
	}

	onChatSend = (e)=> {
		const msg = e.target.value;
		if (new Date().getTime() - this.state.lastTypingSynchedOn.getTime() > this.state.syncDelayInMillis) {
			this.props.handleTypingStatus()
			this.setState({
				lastTypingSynchedOn: new Date()
			})
		}
		this.setState({
			chatMessage: msg,
			emojiButtonClicked: false
		})
	}

	handleSendChat = (e) => {
		e.preventDefault()
		if (this.state.chatMessage) {
			this.props.handleSendChat(this.state.chatMessage)
			this.setState({
				chatMessage: ''
			})	
		}
	}

	render(){
		const {
			className,
			small = false
		} = this.props;

		const cx = classnames(
			c.container, className, 'chatview-footer ui-chat-footer flex-horizontal a-stretch',{
				'is-small': small
			}
		)

		return (
			<div className={cx}>
				<div className='btn btn-default ui-button btn-attachment'>
					<i className='fa fa-paperclip'/>
				</div>
				<div className='btn btn-default ui-button btn-camera'>
					<i className='fa fa-camera-retro'/>
				</div>
				<div className='chat-input-wrap flex-1 flex-horizontal a-stretch'>
					{this.props.showTyping && <div className="chat-user-typing">
						<span>User is typing <i className="fa fa-spin fa-circle-o-notch"></i></span>
					</div>}
					<form onSubmit={this.handleSendChat}>
						<input
							className='chat-input-box'
							type='text'
							placeholder='Type here...'
							spellCheck={true}
							value={this.state.chatMessage}
							onInput={this.onChatSend}/>
						<div className='btn btn-default ui-button chat-input-btn' onClick={this.handleSendChat}>
							<i className='fa fa-paper-plane'/>
						</div>
					</form>
				</div>
				{this.state.emojiButtonClicked && <Picker 
					title='Pick your emoji…' 
					emoji='point_up' 
					style={{ position: 'absolute', bottom: '55px', right: '20px', width: '300px' }}
					showPreview={false}
					emojiSize={20}
					onClick={this.onEmojiClick} />}
				<div className='btn btn-default ui-button' onClick={this.onEmojiButtonClick}>
					<i className='fa fa-smile-o'/>
				</div>
			</div>
		)
	}
}

export default withStyles(c)(ChatFooter)
