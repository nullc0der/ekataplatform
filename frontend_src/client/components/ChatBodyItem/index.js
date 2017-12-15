import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './ChatBodyItem.styl'

import Avatar from 'components/Avatar'

import moment from 'moment'

class ChatBodyItem extends Component {
	render(){
		const {
			className,
			user = {},
			message = '',
			stamp = new Date(),
			left = false
		} = this.props;

		const cx = classnames(c.container, className, 'chat-body-item', {
			'in-left': left
		})

		return (
			<div className={cx}>
				{	
					user.user_image_url ?
                    <img className='img-responsive img-chat-avatar' src={user.user_image_url}/> :
                    <Avatar name={user.username} bgcolor={user.profile_avatar_color} />
                }
				<div className='msg'>
					{message}
					<div className='stamp'>
						{moment(stamp).fromNow()}
					</div>
				</div>

			</div>
		)
	}
}

export default withStyles(c)(ChatBodyItem)
