import {Component} from 'react'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import _ from 'lodash'
import request from 'superagent'
import Websocket from 'react-websocket'

import ChatBodyItem  from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'

import c from './HeaderMiniChat.styl'

import { actions as chatActions, chatsFetchData, sendChat, receivedChatOnWebsocket, deleteChats, sendDeleteChat} from 'store/Chat'
import { updateTypingStatus } from 'store/Chatrooms'

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

		console.log('will min', $chat.get(0))
	}

	handleTypingStatus = (roomId) => {
		request
			.post('/api/messaging/settyping/')
			.set('X-CSRFToken', window.django.csrf)
			.type('form')
			.send({ 'chatroom': roomId })
			.end((err, res) => { })
	}

	renderOneChat = (chat, i)=> {
		const cx = classnames('chat-header', 'flex-horizontal', 'a-center', 'j-between', {'is-online': _.includes(this.props.onlineUsers, chat.username)})
		return <div key={i} className='mini-chat flex-vertical'>
			<div className={cx}>
				<div className='username'> {chat.username} </div>
				<div className='chat-options'>
					{
						this.state.selectedMessages[chat.roomId] && this.state.selectedMessages[chat.roomId].length > 0 && 
						<div
							onClick={() => this.handleDeleteChat(chat.roomId)}
							className='btn btn-default ui-button'>
							<i className='fa fa-trash'/>
						</div>
					}
					<div
						onClick={this.toggleMinimise}
						className='btn btn-default ui-button'>
						<i className='fa fa-window-minimize'/>
					</div>
					<div
						onClick={this.closeChat(chat.roomId)}
						className='btn btn-default ui-button'>
						<i className='fa fa-remove'/>
					</div>
				</div>
			</div>
			<div className='chat-body flex-1'>
				{
					chat.messages.map((x,i)=> {
						return <ChatBodyItem
							key={i}
							roomId={chat.roomId}
							user={x.user}
							message={x.message}
							fileurl={x.fileurl}
							filetype={x.filetype}
							filename={x.filename}
							message_id={x.id}
							stamp={new Date(x.timestamp)}
							left={x.user.username !== window.django.user.username}
							selected={_.includes(this.state.selectedMessages[chat.roomId], x.id)}
							onSelected={this.handleSelectedMessage}/>
					})
				}
			</div>
			<ChatFooter
				small={true}
				roomId={chat.roomId}
				handleSendChat={this.handleSendChat}
				handleTypingStatus={this.handleTypingStatus}
				showTyping={chat.roomId === this.props.websocketTypingStatus}
				showTypingUsername={chat.username}
				uploadProgress={this.props.uploadProgress.roomId === chat.roomId ? this.props.uploadProgress.progress : 0} />
		</div>
	}


	onWebsocketMessage = (data) => {
		const result = JSON.parse(data)
		let messageIds = []
		let roomId = 0
		if (result.add_message) {
			if (this.props.chats[result.chatroom]) {
				this.props.webSocketMessage(result.chatroom, result.message)
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
			for (const data of result) {
				if (this.props.chats[data.chatroom] && !result.add_message) {
					messageIds.push(data.message_id)
					roomId = data.chatroom
				}
			}
			messageIds.length && this.props.deleteChats(roomId, messageIds)
		}
	}


	render(){
		const {className} = this.props;
		const cx = classnames(c.miniChatHolder, 'mini-chat-holder', 'flex-horizontal')
		const websocket_url = `${window.location.protocol == "https:" ? "wss" : "ws"}` + '://' + window.location.host + "/messaging/stream/"
		return (
			<div className={cx}>
				{
					this.state.openChats && this.state.openChats.map(this.renderOneChat)
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
	sendDeleteChats: (url, roomId, chatIds) => dispatch(sendDeleteChat(url, roomId, chatIds))
})

export default connect(mapStateToProps,mapDispatchToProps)(MiniChat)
