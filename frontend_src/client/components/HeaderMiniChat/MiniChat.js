import {Component} from 'react'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import _ from 'lodash'
import request from 'superagent'
import Websocket from 'react-websocket'

import ChatBodyItem  from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'

import c from './HeaderMiniChat.styl'
import MiniChatBox from './MiniChatBox'

import { actions as chatActions, chatsFetchData, sendChat, receivedChatOnWebsocket, deleteChats, sendDeleteChat, updateChatReadStatus} from 'store/Chat'
import { updateTypingStatus, readStatusUpdated } from 'store/Chatrooms'

class MiniChat extends Component {
	constructor(props) {
		super(props)
		this.state = {
			openChats: [],
			selectedMessages: {}
		}
		this.websocketTypingTimeout = null
	}

	componentDidUpdate = (prevProps, prevState) => {
		if (prevProps.chats !== this.props.chats || prevProps.miniChats !== this.props.miniChats) {
			this.filterChats(this.props.chats, this.props.miniChats)
		}
	}

	handleSelectedMessage = (roomId, messageId, shouldSelect) => {
		if (shouldSelect) {
			let messages = [messageId]
			let selectedMessages = this.state.selectedMessages[roomId]
			if (selectedMessages) {
				messages = _.includes(selectedMessages, messageId) ? selectedMessages.filter(x => x !== messageId) : selectedMessages.concat(messageId)
			}
			this.setState(prevState => ({
				selectedMessages: Object.assign({}, prevState.selectedMessages, {[roomId]: messages})
			}))
		}
	}

	filterChats = (chats, miniChats) => {
		let openChats = []
		for (const miniChat of miniChats) {
			if (chats[miniChat]) {
				let chat = {
					username: this.getTitle(miniChat),
					roomId: miniChat,
					messages: chats[miniChat]
				}
				openChats.push(chat)
			} else {
				const url = `/api/messaging/chat/${miniChat}/`
				this.props.fetchData(url, miniChat)
			}
		}
		this.setState({openChats: openChats})
	}

	getTitle = (selected) => {
		for (const room of this.props.rooms) {
			if (room.id === selected) {
				return room.username
			}
		}
	}

	closeChat = (roomId)=> (e)=> {
		this.props.closeMiniChat(roomId)
	}

	handleSendChat = (roomId, content, file = null) => {
		const url = `/api/messaging/chat/${roomId}/`
		this.props.sendChat(url, roomId, content, file)
	}

	handleDeleteChat = (roomId) => {
		if (this.state.selectedMessages[roomId] && this.state.selectedMessages[roomId].length) {
			this.props.sendDeleteChats('/api/messaging/deletemessages/', roomId, this.state.selectedMessages[roomId])
		}
		this.setState(prevState => ({
			selectedMessages: Object.assign({}, prevState.selectedMessages, {[roomId]: []})
		}))
	}

	toggleMinimise = (e)=> {
		var $btn  = $(e.currentTarget)
		var $chat = $btn.parents('.mini-chat')

		if ( $chat.hasClass('is-minimized') ){
			$btn.find('.fa').removeClass('fa-window-maximize').addClass('fa-window-minimize')
			$chat.removeClass('is-minimized')
		} else {
			$btn.find('.fa').removeClass('fa-window-minimize').addClass('fa-window-maximize')
			$chat.addClass('is-minimized')
		}
	}

	handleTypingStatus = (roomId) => {
		request
			.post('/api/messaging/settyping/')
			.set('X-CSRFToken', window.django.csrf)
			.type('form')
			.send({ 'chatroom': roomId })
			.end((err, res) => { })
	}

	handleUnreadChat = (roomId, unreadChats) => {
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
						this.props.updateRoom(roomId)
						this.props.updateChatReadStatus(roomId, chatArr)
					}
				})
		}
	}

	onWebsocketMessage = (data) => {
		const result = JSON.parse(data)
		if (result.add_message) {
			if (this.props.chats[result.chatroom]) {
				this.props.webSocketMessage(result.chatroom, result.message)
			}
			this.props.updateRoom(
				result.chatroom,
				this.props.rooms.filter(x => x.id === result.chatroom)[0].unread_count + 1
			)
			if (this.props.selected !== result.chatroom && !(_.includes(this.props.miniChats, result.chatroom))) {
				$("#messagingaudio")[0].play()
			}
		} else if (result.typing) {
			if (this.websocketTypingTimeout) {
				clearTimeout(this.websocketTypingTimeout)
			}
			this.props.updateTypingStatus(result.chatroom)
			this.websocketTypingTimeout = setTimeout(() => {
				this.props.updateTypingStatus(0)
			}, 5000)
		} else {
			let messageIds = []
			let roomId = 0
			for (const data of result) {
				if (this.props.chats[data.chatroom] && !result.add_message) {
					messageIds.push(data.message_id)
					roomId = data.chatroom
				}
			}
			messageIds.length && this.props.deleteChats(roomId, messageIds) & this.props.updateRoom(
				roomId,
				this.props.rooms.filter(x => x.id === roomId)[0].unread_count - messageIds.length
			)
		}
	}


	render(){
		const {className} = this.props;
		const cx = classnames(c.miniChatHolder, 'mini-chat-holder', 'flex-horizontal')
		const websocket_url = `${window.location.protocol == "https:" ? "wss" : "ws"}` + '://' + window.location.host + "/messaging/stream/"
		return (
			<div className={cx}>
				{
					this.state.openChats && this.state.openChats.map((x, i) => {
						return <MiniChatBox
									key={i}
									chat={x}
									selectedMessages={this.state.selectedMessages}
									uploadProgress={this.props.uploadProgress}
									onlineUsers={this.props.onlineUsers}
									handleDeleteChat={this.handleDeleteChat}
									toggleMinimise={this.toggleMinimise}
									closeChat={this.closeChat}
									handleSelectedMessage={this.handleSelectedMessage}
									handleSendChat={this.handleSendChat}
									handleTypingStatus={this.handleTypingStatus}
									webSocketTypingStatus={this.props.webSocketTypingStatus}
									handleUnreadChat={this.handleUnreadChat} />
					})
				}
				<Websocket url={websocket_url}
					onMessage={this.onWebsocketMessage.bind(this)} />
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	chats: state.Chat.chats,
	rooms: state.ChatRooms.rooms,
	selected: state.ChatRooms.selected,
	miniChats: state.Chat.minichats,
	onlineUsers: state.Users.onlineUsers,
	websocketTypingStatus: state.ChatRooms.websocketTypingStatus,
	uploadProgress: state.Chat.uploadProgress
})

const mapDispatchToProps = (dispatch)=> ({
	closeMiniChat: (id) => dispatch(chatActions.closeMiniChat(id)),
	fetchData: (url, roomId) => dispatch(chatsFetchData(url, roomId)),
	sendChat: (url, roomId, content, file) => dispatch(sendChat(url, roomId, content, file)),
	webSocketMessage: (roomId, chat) => dispatch(receivedChatOnWebsocket(roomId, chat)),
	deleteChats: (roomId, chatIds) => dispatch(deleteChats(roomId, chatIds)),
	updateTypingStatus: (username) => dispatch(updateTypingStatus(username)),
	sendDeleteChats: (url, roomId, chatIds) => dispatch(sendDeleteChat(url, roomId, chatIds)),
	updateChatReadStatus: (roomId, chatIds) => dispatch(updateChatReadStatus(roomId, chatIds)),
	updateRoom: (roomId, unreadCount) => dispatch(readStatusUpdated(roomId, unreadCount)),
})

export default connect(mapStateToProps,mapDispatchToProps)(MiniChat)
