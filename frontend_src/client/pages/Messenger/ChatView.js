import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect} from 'react-redux'
import request from 'superagent'
import _ from 'lodash'

import c from './Messenger.styl'

import ChatBodyItem from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'

import { chatsFetchData, sendChat, sendDeleteChat } from 'store/Chat'
import { readStatusUpdated, sendDeleteRequest } from 'store/Chatrooms'


class ChatView extends Component {
	constructor(props) {
		super(props)
		this.state = {
			selectedMessages: [],
			optionsOpen: false,
			userTyping: false
		}
	}

	componentDidUpdate = (prevProps, prevState) => {
		if (prevProps.selected !== this.props.selected) {
			const url = `/api/messaging/chat/${this.props.selected}/`
			this.props.fetchData(url)
		}
		if (prevProps.chats !== this.props.chats) {
			const chats = this.props.chats
			let unreadIds = chats.filter(x => !x.read)
			if (unreadIds) {
				this.handleUnreadChat(unreadIds)
			}
			this.scrollToBottom()
		}
		if (prevProps.userTyping !== this.props.userTyping) {
			this.setState({
				userTyping: this.props.userTyping == this.props.selected
			})	
		}
	}

	handleUnreadChat = (unreadChats) => {
		let chatArr = []
		for (const unreadChat of unreadChats) {
			chatArr.push(unreadChat.id)
		}
		if (chatArr.length) {
			request
				.post('/en/messaging/setmessagestatus/')
				.set('X-CSRFToken', window.django.csrf)
				.type('form')
				.send({ 'message_ids': chatArr })
				.end((err, res) => {
					if (res.ok) {
						this.props.updateRoom(this.props.selected)
					}
				})
		}
	}

	handleSelectedMessage = (messageId, shouldSelect) => {
		if (shouldSelect) {
			let selectedMessages = this.state.selectedMessages
			let messages = _.includes(selectedMessages, messageId) ? selectedMessages.filter(x => x !== messageId) : selectedMessages.concat(messageId)
			this.setState({
				selectedMessages: messages
			})	
		}
	}

	handleOptions = () => {
		this.setState(prevState => ({
			optionsOpen: !prevState.optionsOpen
		}))
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

	handleDelete = (e) => {
		e.preventDefault()
		this.props.deleteRoom('/en/messaging/deleteroom/', this.props.selected)
		this.props.selectNext()
		this.setState(prevState => ({
			optionsOpen: !prevState.optionsOpen
		}))
	}

	handleDeleteChat = (e) => {
		e.preventDefault()
		if (this.state.selectedMessages.length) {
			this.props.deleteChats('/api/messaging/deletemessages/', this.state.selectedMessages)	
		}
		this.setState(prevState => ({
			optionsOpen: !prevState.optionsOpen
		}))
	}

	handleTypingStatus = () => {
		request
			.post('/api/messaging/settyping/')
			.set('X-CSRFToken', window.django.csrf)
			.type('form')
			.send({ 'chatroom': this.props.selected })
			.end((err, res) => {})
	}

	handleDialogs = (e) => {
		if (this.state.optionsOpen) {
			this.setState({
				optionsOpen: false
			})
		}
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

	renderOptions = () => {
		const deleteString = this.state.selectedMessages.length > 1 ? 'Delete Selected Messages' : 'Delete Selected Message'
		return (
			<ul className="dropdown-menu animated fadeIn" style={{ left: "auto", right: 0 }}>
				<li><a href='#' onClick={this.handleDelete}>Delete This Room</a></li>
				{this.state.selectedMessages.length > 0 && <li><a href='#' onClick={this.handleDeleteChat}>{deleteString}</a></li>}
			</ul>
		)
	}

	render(){
		const {
			className,
			chats,
			title
		} = this.props;

		const cx = classnames(c.chatView, className, 'flex-vertical')

		return (
			<div className={cx} onClick={this.handleDialogs}>
				<div className='chatview-header flex-horizontal a-center'>
					{/*<div className='text-muted text-session-id'> Session ID: #3949aaudh1 </div>*/}
					<div className='text-username text-center flex-1'> {title} </div>
					<div className='header-options'>
						<div className={this.state.optionsOpen ? "dropdown open" : "dropdown"}>
							{this.renderOptions()}
						</div>
						<div className='btn btn-default ui-button' onClick={this.handleOptions}>
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
								message_id={x.id}
								stamp={new Date(x.timestamp)}
								left={x.user.username !== window.django.user.username}
								selected={_.includes(this.state.selectedMessages, x.id)}
								onSelected={this.handleSelectedMessage}/>
						})
					}
					<div style={{ float:"left", clear: "both" }}
             			ref={(el) => { this.messagesEnd = el; }}>
        			</div>
				</div>
				<ChatFooter 
					handleSendChat={this.handleSendChat}
					handleTypingStatus={this.handleTypingStatus}
					showTyping={this.state.userTyping}
					showTypingUsername={title} />
			</div>
		)
	}
}

ChatView.propTypes = {
	chats: PropTypes.array.isRequired,
	selected: PropTypes.number.isRequired,
	areLoading: PropTypes.bool.isRequired,
	hasErrored: PropTypes.bool.isRequired,
	fetchData: PropTypes.func.isRequired,
	sendChat: PropTypes.func.isRequired,
	updateRoom: PropTypes.func.isRequired,
	deleteRoom: PropTypes.func.isRequired,
	deleteChats: PropTypes.func.isRequired
}

const mapStateToProps = (state)=> ({
	chats: state.Chat.chats,
	selected: state.ChatRooms.selected,
	areLoading: state.Chat.areLoading,
	hasErrored: state.Chat.hasErrored
})
const mapDispatchToProps = (dispatch)=> ({
	fetchData: (url) => dispatch(chatsFetchData(url)),
	sendChat: (url, content) => dispatch(sendChat(url, content)),
	updateRoom: (roomId) => dispatch(readStatusUpdated(roomId)),
	deleteRoom: (url, roomId) => dispatch(sendDeleteRequest(url, roomId)),
	deleteChats: (url, chatIds) => dispatch(sendDeleteChat(url, chatIds))
})

export default connect(mapStateToProps,mapDispatchToProps)(ChatView)
