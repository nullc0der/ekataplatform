import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import Helmet from 'react-helmet'
import { connect } from 'react-redux'

import NotificationHeader from 'components/NotificationHeader'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Members.styl'
import { actions as groupNotificationAction } from 'store/GroupNotifications'

import MembersManagement from './MembersManagement'
import NotificationCenter from './NotificationCenter'

class MembersPage extends Component {

	componentDidMount() {
		const id = this.props.params.id
		this.props.loadNotifications(`/api/groups/${id}/notifications/`)
	}

	render(){
		const {
			className
		} = this.props;

		const cx = classnames(c.container, className, 'flex-vertical flex-1')

		const managementClass = classnames(c.management, 'flex-1')
		const notificationClass  = classnames(c.notifications, 'flex-1')
		return (
			<div className={cx}>
				<Helmet title={`Group | ${this.props.params.id} | Member`}/>
				{this.props.notifications.length > 0 && <NotificationHeader notifications={this.props.notifications} />}
				<div className='member-boxes-wrapper'>
					<MembersManagement
						className={managementClass}
						groupID={this.props.params.id} />
					<div className='boxes-in-right flex-vertical'>
						<NotificationCenter
							className={notificationClass}
							groupID={this.props.params.id} />
					</div>
				</div>
			</div>
		)
	}
}

const mapStateToProps = (state) => ({
	notifications: state.GroupNotifications.notifications
})

const mapDispatchToProps = (dispatch) => ({
	loadNotifications: (url) => dispatch(groupNotificationAction.loadNotifications(url)),
})

export default withStyles(c)(
	connect(mapStateToProps, mapDispatchToProps)(MembersPage))
