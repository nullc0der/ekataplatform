import {Component} from 'react'
import classnames  from 'classnames'
import { connect } from 'react-redux'
import Websocket from 'react-websocket'

import Avatar from 'components/Avatar'
import NotificationItem from './NotificationItem'
import { actions as memberActions } from 'store/Members'
import { actions as groupMemberNotificationActions } from 'store/GroupMemberNotification'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './NotificationCenter.styl'

class NotificationCenter extends Component {

	state = {
		activeNode: null
	}

	componentDidMount() {
		const id = this.props.groupID
		this.props.loadNotifications(`/api/groups/${id}/mynotifications/`)
	}

	componentDidUpdate(prevProps) {
		if (prevProps.groupID !== this.props.groupID) {
			const id = this.props.groupID
			this.props.loadNotifications(`/api/groups/${id}/mynotifications/`)
		}
	}

	acceptDenyJoinRequest = (notificationID, requestID, accept) => {
		const id = this.props.groupID
		this.props.acceptDenyJoinRequest(
			`/api/groups/${id}/joinrequests/${requestID}/`,
			notificationID,
			accept
		)
	}

	setNotificationRead = (notificationID) => {
		const id = this.props.groupID
		this.props.setNotificationRead(
			`/api/groups/${id}/mynotifications/`,
			notificationID
		)	
	}

	setActiveNode = (id) => {
		this.setState({
			activeNode: id
		})
	}

	onWebsocketMessage = (data) => {
		const result = JSON.parse(data)
		if (result.group_id == this.props.groupID) {
			this.props.receivedWebsocketNotification(result.notification)
		}
	}

	render(){
		const {
			className,
			notifications
		} = this.props;

		const cx = classnames(className, c.container, 'flex-vertical')
		const websocket_url = `${window.location.protocol == "https:" ? "wss" : "ws"}` + '://' + window.location.host + "/groupnotifications/stream/"

		return (
			<div className={cx}>
				<div className='nc-header'>
					Notification Center
				</div>
				<div className='nc-list flex-1 scroll-y'>
					{
						notifications.map((x, i) => {
							return (
								<NotificationItem 
									key={i} notification={x} isActive={this.state.activeNode === x.id}
									setActiveNode={this.setActiveNode}
									acceptDenyJoinRequest={this.acceptDenyJoinRequest}
									setNotificationRead={this.setNotificationRead}/>
							)
						})
					}
				</div>
				<Websocket url={websocket_url}
					onMessage={this.onWebsocketMessage.bind(this)} />
			</div>
		)
	}
}

const mapStateToProps = (state) => ({
	notifications: state.GroupMemberNotification.notifications
})

const mapDispatchToProps = (dispatch) => ({
	acceptDenyJoinRequest: (url, notificationID, accepted) => {
		dispatch(memberActions.acceptDenyJoinRequest(url, notificationID, accepted))
	},
	loadNotifications: (url) => {
		dispatch(groupMemberNotificationActions.loadMemberNotifications(url))
	},
	setNotificationRead: (url, notificationID) => {
		dispatch(groupMemberNotificationActions.setNotificationRead(url, notificationID))
	},
	receivedWebsocketNotification: (notification) => {
		dispatch(groupMemberNotificationActions.receivedWebsocketNotification(notification))
	}
})

export default withStyles(c)(
	connect(mapStateToProps, mapDispatchToProps)(NotificationCenter)
)
