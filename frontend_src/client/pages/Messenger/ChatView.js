import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect} from 'react-redux'

import c from './Messenger.styl'

import ChatBodyItem from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'

import { chatsFetchData, sendChat } from 'store/Chat'


class ChatView extends Component {
	componentDidUpdate = (prevProps, prevState) => {
		if (prevProps.selected !== this.props.selected) {
			const url = `/api/messaging/chat/${this.props.selected}/`
			this.props.fetchData(url)	
		}
		this.scrollToBottom()
	}

	componentDidMount = () => {
		this.scrollToBottom()
	}

	scrollToBottom = () => {
		this.messagesEnd.scrollIntoView({ behavior: "smooth" })
	}

	closeChatView = ()=> {
		$('.' + c.chatView).toggleClass('is-open')
	}

	handleSendChat = (content) => {
		const url = `/api/messaging/chat/${this.props.selected}/`
		this.props.sendChat(url, content)
	}

	sendDemoChat = (e)=> {
		// if (e.keyCode !== 13)
		// 	return

		var val = $('.chat-input-box').val()
		var $chat = $('<div/>', {class: 'chat-body-item'}).text(val)
		$('.chatview-body').append(
			$chat
		)

		$chat.get(0).scrollIntoView();
	}

	render(){
		const {
			className,
			chats,
			title
		} = this.props;

		const cx = classnames(c.chatView, className, 'flex-vertical')

		return (
			<div className={cx}>
				<div className='chatview-header flex-horizontal a-center'>
					{/*<div className='text-muted text-session-id'> Session ID: #3949aaudh1 </div>*/}
					<div className='text-username text-center flex-1'> {title} </div>
					<div className='header-options'>
						<div className='btn btn-default ui-button'>
							<i className='fa fa-ellipsis-v'/>
						</div>
						<div onClick={this.closeChatView} className='btn btn-default btn-chat ui-button mobile-close-chat'>
							<i className='fa fa-remove'/>
						</div>
					</div>
				</div>
				<div className='chatview-body flex-1'>
					{
						chats.map((x, i)=> {
							return <ChatBodyItem
								key={i}
								user={x.user}
								message={x.message}
								stamp={new Date(x.timestamp)}
								left={x.user.username !== window.django.user.username}/>
						})
					}
					<div style={{ float:"left", clear: "both" }}
             			ref={(el) => { this.messagesEnd = el; }}>
        			</div>
				</div>
				<ChatFooter handleSendChat={this.handleSendChat}/>
			</div>
		)
	}
}

ChatView.propTypes = {
	chats: PropTypes.array.isRequired,
	selected: PropTypes.number.isRequired,
	areLoading: PropTypes.bool.isRequired,
	hasErrored: PropTypes.bool.isRequired,
	fetchData: PropTypes.func.isRequired
}

const mapStateToProps = (state)=> ({
	chats: state.Chat.chats,
	selected: state.ChatRooms.selected,
	areLoading: state.Chat.areLoading,
	hasErrored: state.Chat.hasErrored
})
const mapDispatchToProps = (dispatch)=> ({
	fetchData: (url) => dispatch(chatsFetchData(url)),
	sendChat: (url, content) => dispatch(sendChat(url, content))
})

export default connect(mapStateToProps,mapDispatchToProps)(ChatView)
