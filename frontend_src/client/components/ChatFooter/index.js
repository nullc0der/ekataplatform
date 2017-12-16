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
			chatMessage: ''
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
		console.log('sending chat: ', msg)
		this.setState({
			chatMessage: msg
		})
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
					<input
						className='chat-input-box'
						type='text'
						placeholder='Type here...'
						value={this.state.chatMessage}
						onInput={this.onChatSend}/>
					<div className='btn btn-default ui-button chat-input-btn'>
						<i className='fa fa-paper-plane'/>
					</div>
				</div>
				{this.state.emojiButtonClicked && <Picker 
					title='Pick your emoji…' 
					emoji='point_up' 
					style={{ position: 'absolute', bottom: '55px', right: '20px' }}
					onClick={this.onEmojiClick} />}
				<div className='btn btn-default ui-button' onClick={this.onEmojiButtonClick}>
					<i className='fa fa-smile-o'/>
				</div>
			</div>
		)
	}
}

export default withStyles(c)(ChatFooter)
