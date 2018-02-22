import {Component} from 'react'
import { connect } from 'react-redux'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import Websocket from 'react-websocket'

import Avatar from 'components/Avatar'
import { actions as memberActions } from 'store/Members'
import { actions as groupNotificationActions } from 'store/GroupNotifications'
import NotificationItem from './NotificationItem'

import c from './Members.styl'

class NotificationCenter extends Component {

	state = {
		activeNode: null
	}
	
	componentDidMount = () => {
		const id = this.props.groupID
		this.props.getJoinRequests(`/api/groups/${id}/joinrequests/`)
		this.props.getGroupNotifications(`/api/groups/${id}/notifications/`)
	}

	acceptDenyJoinRequest = (requestID, accept) => {
		const id = this.props.groupID
		this.props.acceptDenyJoinRequest(
			`/api/groups/${id}/joinrequests/${requestID}/`,
			requestID,
			accept
		)
	}

	onWebsocketMessage = (data) => {
		const result = JSON.parse(data)
		if (result.group_id == this.props.groupID) {
			this.props.receivedJoinRequest(result.req)
		}
	}

	setActiveNode = (id) => {
		this.setState({
			activeNode: id
		})
	}

	render(){
		const {
			className,
			joinRequests,
			notifications
		} = this.props;

		const cx = classnames(className, 'flex-vertical')
		const websocket_url = `${window.location.protocol == "https:" ? "wss" : "ws"}` + '://' + window.location.host + "/groupnotifications/stream/"

		return (
			<div className={cx}>
				<div className='nc-header'>
					Notification Center
				</div>
				<div className='nc-list flex-1 scroll-y'>
					{
						joinRequests.map((x, i)=> {
							return <div key={i} className='nc-list-item flex-horizontal a-center'>
								<a href={x.user.public_url}>
									{
										x.user.avatar_url ?
											<img className='avatar-image rounded' src={x.user.avatar_url} /> :
											<Avatar className='avatar-image' name={x.user.fullname || x.user.username} bgcolor={x.user.user_avatar_color} />
									}
								</a>
								<div className='details'>
									<div className='name'> {x.user.fullname || x.user.username } </div>
									<div className='subtext'> Sent a request to join </div>
								</div>
								<div className='flex-1'/>
								{
									<div className='nf-btn btn-accept' onClick={(e) => this.acceptDenyJoinRequest(x.id, true)}>
										Accept
									</div>
								}
								{
									<div className='nf-btn btn-deny' onClick={(e) => this.acceptDenyJoinRequest(x.id, false)}>
										Deny
									</div>
								}
							</div>
						})
					}
					{
						notifications.map((x, i) => {
							return (
								<NotificationItem 
									key={i} notification={x} isActive={this.state.activeNode === x.id}
									setActiveNode={this.setActiveNode}/>
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
	joinRequests: state.Members.joinRequests,
	notifications: state.GroupNotifications.notifications
})

const mapDispatchToProps = (dispatch) => ({
	getJoinRequests: (url) => {
		dispatch(memberActions.getJoinRequests(url))
	},
	acceptDenyJoinRequest: (url, requestID, accepted) => {
		dispatch(memberActions.acceptDenyJoinRequest(url, requestID, accepted))
	},
	receivedJoinRequest: (joinRequest) => {
		dispatch(memberActions.receivedJoinRequestOnWebsocket(joinRequest))
	},
	getGroupNotifications: (url) => {
		dispatch(groupNotificationActions.loadNotifications(url))
	}
})

export default connect(
	mapStateToProps, mapDispatchToProps
)(NotificationCenter)
