import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import Helmet from 'react-helmet'
import { connect } from 'react-redux'
import _ from 'lodash'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Messenger.styl'

import Sidebar  from './Sidebar'
import ChatView from './ChatView'

import { roomsFetchData, roomSelected, searchTextChanged } from 'store/Chatrooms'
import { clearChat, actions } from 'store/Chat'
import { actions as commonActions } from 'store/Common'

class Messenger extends Component {

	componentDidMount = ()=> {
		this.props.fetchData('/api/messaging/chatrooms/', true)
	}

	componentDidUpdate = (prevProps) => {
		if (prevProps.params.id !== this.props.params.id) {
			this.onSidebarChatSelect(parseInt(this.props.params.id))
		}
	}

	onSidebarChatSelect = (id)=> {
		this.props.selectRoom(id)
		$('.' + c.chatView).addClass('is-open')
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

	selectNextRoom = () => {
		this.props.clearChat(this.props.selected)
		if (_.includes(this.props.miniChats, this.props.selected)) {
			this.props.closeMiniChat(this.props.selected)
		}
		for (const room of this.props.rooms) {
			if (room.id > this.props.selected || room.id < this.props.selected) {
				this.props.selectRoom(room.id)
			}
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

		const cx = classnames(c.container, className, 'flex-horizontal', 'a-stretch', 'flex-1')
		const title = this.getTitle(rooms, selected)
		return (
			<div className={cx}>
				<Helmet title="Messenger" />
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
					userTyping = {this.props.websocketTypingStatus}
					/>
			</div>
		)
	}
}

Messenger.propTypes = {
	rooms: PropTypes.array.isRequired,
	chats: PropTypes.object.isRequired,
	onlineUsers: PropTypes.array.isRequired,
	websocketTypingStatus: PropTypes.number.isRequired,
	areLoading: PropTypes.bool.isRequired,
	hasErrored: PropTypes.bool.isRequired,
	selected: PropTypes.number.isRequired,
	miniChats: PropTypes.array.isRequired,
	fetchData: PropTypes.func.isRequired,
	selectRoom: PropTypes.func.isRequired,
	changeSearchText: PropTypes.func.isRequired,
	clearChat: PropTypes.func.isRequired,
	closeMiniChat: PropTypes.func.isRequired
}

const filterRooms = (rooms, searchText) => {
	if(searchText) {
		return rooms.filter((room) => room.username.toLowerCase().startsWith(searchText.toLowerCase()))
	}
	return rooms
}

const mapStateToProps = (state) => ({
	rooms: filterRooms(state.ChatRooms.rooms, state.ChatRooms.searchText),
	chats: state.Chat.chats,
	selected: state.ChatRooms.selected,
	miniChats: state.Chat.minichats,
	areLoading: state.ChatRooms.areLoading,
	hasErrored: state.ChatRooms.hasErrored,
	onlineUsers: state.Users.onlineUsers,
	websocketTypingStatus: state.ChatRooms.websocketTypingStatus
})

const mapDispatchToProps = (dispatch) => ({
	fetchData: (url, selectFirst) => dispatch(roomsFetchData(url, selectFirst)),
	selectRoom: (id) => dispatch(roomSelected(id)),
	changeSearchText: (searchText) => dispatch(searchTextChanged(searchText)),
	clearChat: (roomId) => dispatch(clearChat(roomId)),
	closeMiniChat: (roomId) => dispatch(actions.closeMiniChat(roomId)),
	updateHeaderVisibility: (showHeaders) => dispatch(commonActions.updateHeaderVisibility(showHeaders))
})

export default withStyles(c)(
	connect(mapStateToProps, mapDispatchToProps)(Messenger)
)
