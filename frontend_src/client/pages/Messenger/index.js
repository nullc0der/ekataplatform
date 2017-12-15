import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import { connect } from 'react-redux'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Messenger.styl'

import Sidebar  from './Sidebar'
import ChatView from './ChatView'

import { roomsFetchData, roomSelected, searchTextChanged } from 'store/Chatrooms'

import SAMPLE_CHATS from './sample-chats'
import SAMPLE_DETAILED_CHAT from './sample-detailed-chat'

class Messenger extends Component {
	componentDidMount = ()=> {
		this.props.fetchData('/api/messaging/chatrooms/')
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

	render(){
		const {
			className,
			rooms,
			selected,
			hasErrored
		} = this.props;
		
		const cx = classnames(c.container, className, 'flex-horizontal', 'a-stretch', 'flex-1')
		const title = this.getTitle(rooms, selected)
		return (
			<div className={cx}>
				<Sidebar
					selected={selected}
					hasErrored={hasErrored}
					onItemClick={this.onSidebarChatSelect}
					onSearchChange={this.onSearchInputChange}
					items={rooms}/>
				<ChatView
					title = {this.getTitle(rooms, selected)}
					/>
			</div>
		)
	}
}

Messenger.propTypes = {
	rooms: PropTypes.array.isRequired,
	areLoading: PropTypes.bool.isRequired,
	hasErrored: PropTypes.bool.isRequired,
	selected: PropTypes.number.isRequired,
	fetchData: PropTypes.func.isRequired,
	selectRoom: PropTypes.func.isRequired,
	changeSearchText: PropTypes.func.isRequired
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
	hasErrored: state.ChatRooms.hasErrored
})

const mapDispatchToProps = (dispatch) => ({
	fetchData: (url) => dispatch(roomsFetchData(url)),
	selectRoom: (id) => dispatch(roomSelected(id)),
	changeSearchText: (searchText) => dispatch(searchTextChanged(searchText))
})

export default withStyles(c)(
	connect(mapStateToProps, mapDispatchToProps)(Messenger)
)
