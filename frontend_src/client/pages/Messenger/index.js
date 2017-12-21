import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import { connect } from 'react-redux'
import Websocket   from 'react-websocket'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Messenger.styl'

import Sidebar  from './Sidebar'
import ChatView from './ChatView'

import { roomsFetchData, roomSelected, searchTextChanged } from 'store/Chatrooms'
import { receivedChatOnWebsocket, clearChat, deleteChats } from 'store/Chat'
import { fetchOnlineUsers } from 'store/Users'

import SAMPLE_CHATS from './sample-chats'
import SAMPLE_DETAILED_CHAT from './sample-detailed-chat'

class Messenger extends Component {

	constructor(props) {
		super(props)
		this.state = {
			websocketTypingStatus: null
		}
		this.websocketTypingTimeout = null
	}

	componentDidMount = ()=> {
		this.props.fetchData('/api/messaging/chatrooms/')
		this.onlineGetter = setInterval(
			() => this.props.fetchOnlineUsersList('/onlineusers/'),
			20000
		)
	}

	componentWillUnmount() {
		clearInterval(this.onlineGetter)
	}

	onSidebarChatSelect = (id)=> {
		console.log('clicked something: ', id)
		this.props.selectRoom(id)
		$('.' + c.chatView).toggleClass('is-open')
	}

	onSearchInputChange = (e) => {
		this.props.changeSearchText(e.target.value)
	}

	getTitle = (rooms, selected) => {
		for (const room of rooms) {
			if (room.id === selected) {
				return room.username
			}
		}
	}

	onWebsocketMessage = (data) => {
		const result = JSON.parse(data)
		let messageIds = []
		if (result.add_message) {
			if (result.chatroom === this.props.selected) {
				this.props.webSocketMessage(result.message)
			}	
		} else if(result.typing) {
			if (this.websocketTypingTimeout) {
				clearTimeout(this.websocketTypingTimeout)
			}
			this.setState({
				websocketTypingStatus: result.chatroom
			})
			this.websocketTypingTimeout = setTimeout(() => {
				this.setState({
					websocketTypingStatus: ""
				})
			}, 5000)
		} else {
			for (const data of result) {
				if (data.chatroom === this.props.selected && !result.add_message) {
					messageIds.push(data.message_id)
				}
			}
			messageIds.length && this.props.deleteChats(messageIds)
		}
	}

	selectNextRoom = () => {
		for (const room of this.props.rooms) {
			if (room.id > this.props.selected || room.id < this.props.selected) {
				this.props.selectRoom(room.id)
			}
			this.props.clearChat(0)
		}
	}

	render(){
		const {
			className,
			rooms,
			selected,
			hasErrored,
			onlineUsers
		} = this.props;
		
		const websocket_url = `${window.location.protocol == "https:" ? "wss" : "ws"}` + '://' + window.location.host + "/messaging/stream/"
		const cx = classnames(c.container, className, 'flex-horizontal', 'a-stretch', 'flex-1')
		const title = this.getTitle(rooms, selected)
		return (
			<div className={cx}>
				<Sidebar
					selected={selected}
					hasErrored={hasErrored}
					onItemClick={this.onSidebarChatSelect}
					onSearchChange={this.onSearchInputChange}
					items={rooms}
					onlineUsers={onlineUsers}/>
				<ChatView
					title = {this.getTitle(rooms, selected)}
					selectNext = {this.selectNextRoom}
					userTyping = {this.state.websocketTypingStatus}
					/>
				<Websocket url={websocket_url}
              		onMessage={this.onWebsocketMessage.bind(this)}/>
			</div>
		)
	}
}

Messenger.propTypes = {
	rooms: PropTypes.array.isRequired,
	onlineUsers: PropTypes.array.isRequired,
	areLoading: PropTypes.bool.isRequired,
	hasErrored: PropTypes.bool.isRequired,
	selected: PropTypes.number.isRequired,
	fetchData: PropTypes.func.isRequired,
	selectRoom: PropTypes.func.isRequired,
	changeSearchText: PropTypes.func.isRequired,
	webSocketMessage: PropTypes.func.isRequired,
	fetchOnlineUsersList: PropTypes.func.isRequired,
	clearChat: PropTypes.func.isRequired,
	deleteChats: PropTypes.func.isRequired
}

const filterRooms = (rooms, searchText) => {
	if(searchText) {
		return rooms.filter((room) => room.username.toLowerCase().startsWith(searchText.toLowerCase()))
	}
	return rooms
}

const mapStateToProps = (state) => ({
	rooms: filterRooms(state.ChatRooms.rooms, state.ChatRooms.searchText),
	selected: state.ChatRooms.selected,
	areLoading: state.ChatRooms.areLoading,
	hasErrored: state.ChatRooms.hasErrored,
	onlineUsers: state.Users.onlineUsers
})

const mapDispatchToProps = (dispatch) => ({
	fetchData: (url) => dispatch(roomsFetchData(url)),
	selectRoom: (id) => dispatch(roomSelected(id)),
	changeSearchText: (searchText) => dispatch(searchTextChanged(searchText)),
	webSocketMessage: (chat) => dispatch(receivedChatOnWebsocket(chat)),
	fetchOnlineUsersList: (url) => dispatch(fetchOnlineUsers(url)),
	clearChat: (roomId) => dispatch(clearChat(roomId)),
	deleteChats: (chatIds) => dispatch(deleteChats(chatIds))
})

export default withStyles(c)(
	connect(mapStateToProps, mapDispatchToProps)(Messenger)
)
