import {Component} from 'react'
import classnames  from 'classnames'


class ChatSidebarItem extends Component {
	render(){
		const {
			selected = false,
			username = '',
			status = '',
			num_unread = '',
			image = false
		}  = this.props;

		const cx = classnames('chat-sidebar-item', {
			'is-active': selected
		})
		const statusKey = 'is-' + status.toLowerCase();

		return (
			<div className={cx} onClick={this.props.onClick}>
				<div className='item-image rounded black-bg'>
				</div>
				<div className='item-details'>
					<div className='item-username'> {username} </div>
					<div className='item-status flex-horizontal a-center'>
						<div className={`flex-1 online-status ${statusKey}`}> {status} </div>
						<div className='unread-count'>
							{num_unread} Unread
						</div>
					</div>
				</div>
			</div>
		)
	}
}

export default ChatSidebarItem