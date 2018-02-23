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
		this.props.getGroupNotifications(`/api/groups/${id}/notifications/`)
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
									setActiveNode={this.setActiveNode}/>
							)
						})
					}
				</div>
			</div>
		)
	}
}

const mapStateToProps = (state) => ({
	notifications: state.GroupNotifications.notifications
})

const mapDispatchToProps = (dispatch) => ({
	getGroupNotifications: (url) => {
		dispatch(groupNotificationActions.loadNotifications(url))
	}
})

export default connect(
	mapStateToProps, mapDispatchToProps
)(NotificationCenter)
