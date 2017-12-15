import {Component} from 'react'
import classnames  from 'classnames'
import Avatar from 'components/Avatar'


class ChatSidebarItem extends Component {
	render(){
		const {
			selected = false,
			username = '',
			is_online = false,
			num_unread = '',
			image = false,
			avatar_color=''
		}  = this.props;

		const cx = classnames('chat-sidebar-item', {
			'is-active': selected
		})
		const status = `${is_online ? 'Online': 'Offline'}`
		const statusKey = 'is-' + status

		return (
			<div className={cx} onClick={this.props.onClick}>
				<div className='item-image rounded'>
					{
                        image ?
                        <img className='img-responsive' src={image}/> :
                        <Avatar name={username} bgcolor={avatar_color} fontsize="2em"/>
                    }
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
