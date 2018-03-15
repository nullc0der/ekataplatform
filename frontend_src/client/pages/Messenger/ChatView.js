import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect} from 'react-redux'
import request from 'superagent'
import _ from 'lodash'
import Swipeable from 'react-swipeable'

import c from './Messenger.styl'

import ChatBodyItem from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'

import { chatsFetchData, sendChat, sendDeleteChat, updateChatReadStatus } from 'store/Chat'
import { readStatusUpdated, sendDeleteRequest } from 'store/Chatrooms'
import { actions as commonActions } from 'store/Common'


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
		const chats = this.props.chats[this.props.selected]
		if (prevProps.selected !== this.props.selected) {
			if (!chats) {
				const url = `/api/messaging/chat/${this.props.selected}/`
				this.props.fetchData(url, this.props.selected)	
			} else {
				let unreadIds = chats.filter(x => !x.read & x.user.username !== window.django.user.username)
				if (unreadIds) {
					this.handleUnreadChat(unreadIds)
				}
				this.scrollToBottom()
			}
		}
		if (prevProps.chats[this.props.selected] !== this.props.chats[this.props.selected]) {
			let unreadIds = chats.filter(x => !x.read & x.user.username !== window.django.user.username)
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
						this.props.updateChatReadStatus(this.props.selected, chatArr)
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
		$('.' + c.chatView).removeClass('is-open fullscreen')
		if ($(window).width() < 768) {
			this.props.updateHeaderVisibility(true)
		}
	}

	handleSendChat = (content, file=null) => {
		const url = `/api/messaging/chat/${this.props.selected}/`
		this.props.sendChat(url, this.props.selected, content, file)
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
			this.props.deleteChats('/api/messaging/deletemessages/', this.props.selected, this.state.selectedMessages)	
		}
		this.setState(prevState => ({
			optionsOpen: !prevState.optionsOpen,
			selectedMessages: []
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

	renderOptions = () => {
		const deleteString = this.state.selectedMessages.length > 1 ? `Delete Selected Messages (${this.state.selectedMessages.length})` : 'Delete Selected Message'
		return (
			<ul className="dropdown-menu animated fadeIn" style={{ left: "auto", right: 0 }}>
				<li><a href='#' onClick={this.handleDelete}>Delete This Room</a></li>
				{this.state.selectedMessages.length > 0 && <li><a href='#' onClick={this.handleDeleteChat}>{deleteString}</a></li>}
			</ul>
		)
	}

	chatViewBodySwipedDown = (e, deltaY, isFlick) => {
		if (isFlick && $(window).width() < 768) {
			this.props.updateHeaderVisibility(true)
			$('.' + c.chatView).removeClass('fullscreen')
		}
	}

	chatViewBodySwipedUp = (e, deltaY, isFlick) => {
		if (isFlick && $(window).width() < 768) {
			this.props.updateHeaderVisibility(false)
			$('.' + c.chatView).addClass('fullscreen')
		}
	}

	chatFooterInputFocus = () => {
		if ($(window).width() < 768) {
			this.props.updateHeaderVisibility(false)
			$('.' + c.chatView).addClass('fullscreen')
		}
	}

	render(){
		const {
			className,
			chats,
			title,
			selected
		} = this.props;

		const cx = classnames(c.chatView, className, 'flex-vertical')
		const chat = chats[selected]

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
							<i className='fas fa-ellipsis-v'/>
						</div>
						<div onClick={this.closeChatView} className='btn btn-default btn-chat ui-button mobile-close-chat'>
							<i className='fas fa-times'/>
						</div>
					</div>
				</div>
				<Swipeable className='chatview-body flex-1' onSwipedDown={this.chatViewBodySwipedDown} onSwipedUp={this.chatViewBodySwipedUp}>
					{
						chat &&
						chat.map((x, i) => {
							return <ChatBodyItem
								key={i}
								user={x.user}
								message={x.message}
								fileurl={x.fileurl}
								filetype={x.filetype}
								filename={x.filename}
								message_id={x.id}
								stamp={new Date(x.timestamp)}
								left={x.user.username !== window.django.user.username}
								selected={_.includes(this.state.selectedMessages, x.id)}
								onSelected={this.handleSelectedMessage} />
						})
					}
					<div style={{ float: "left", clear: "both" }}
						ref={(el) => { this.messagesEnd = el; }}>
					</div>
				</Swipeable>
				<ChatFooter 
					handleSendChat={this.handleSendChat}
					handleTypingStatus={this.handleTypingStatus}
					showTyping={this.state.userTyping}
					showTypingUsername={title}
					uploadProgress={this.props.uploadProgress.roomId === selected ? this.props.uploadProgress.progress: 0}
					onChatInputFocus={this.chatFooterInputFocus} />
			</div>
		)
	}
}

ChatView.propTypes = {
	chats: PropTypes.object.isRequired,
	selected: PropTypes.number.isRequired,
	areLoading: PropTypes.bool.isRequired,
	hasErrored: PropTypes.bool.isRequired,
	fetchData: PropTypes.func.isRequired,
	sendChat: PropTypes.func.isRequired,
	updateRoom: PropTypes.func.isRequired,
	deleteRoom: PropTypes.func.isRequired,
	deleteChats: PropTypes.func.isRequired,
	updateHeaderVisibility: PropTypes.func.isRequired,
	updateChatReadStatus: PropTypes.func.isRequired,
	uploadProgress: PropTypes.object
}

const mapStateToProps = (state)=> ({
	chats: state.Chat.chats,
	selected: state.ChatRooms.selected,
	areLoading: state.Chat.areLoading,
	hasErrored: state.Chat.hasErrored,
	uploadProgress: state.Chat.uploadProgress
})

const mapDispatchToProps = (dispatch)=> ({
	fetchData: (url, roomId) => dispatch(chatsFetchData(url, roomId)),
	sendChat: (url, roomId, content, file) => dispatch(sendChat(url, roomId, content, file)),
	updateRoom: (roomId) => dispatch(readStatusUpdated(roomId)),
	deleteRoom: (url, roomId) => dispatch(sendDeleteRequest(url, roomId)),
	deleteChats: (url, roomId, chatIds) => dispatch(sendDeleteChat(url, roomId, chatIds)),
	updateHeaderVisibility: (showHeaders) => dispatch(commonActions.updateHeaderVisibility(showHeaders)),
	updateChatReadStatus: (roomId, chatIds) => dispatch(updateChatReadStatus(roomId, chatIds))
})

export default connect(mapStateToProps,mapDispatchToProps)(ChatView)
