import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Members.styl'

import MembersManagement from './MembersManagement'
import NotificationCenter from './NotificationCenter'

class MembersPage extends Component {
	render(){
		const {
			className
		} = this.props;

		const cx = classnames(c.container, className, 'flex-horizontal flex-1')

		const managementClass = classnames(c.management, 'flex-1')
		const notificationClass  = classnames(c.notifications, 'flex-1')
		return (
			<div className={cx}>
				<MembersManagement
					className={managementClass}/>
				<div className='boxes-in-right flex-vertical'>
					<NotificationCenter
						className={notificationClass}/>
				</div>
			</div>
		)
	}
}

export default withStyles(c)(MembersPage)
