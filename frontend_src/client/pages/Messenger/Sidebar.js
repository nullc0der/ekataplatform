import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import _ from 'lodash'

import c from './Messenger.styl'

import ChatSidebarItem from './ChatSidebarItem'

class Sidebar extends Component {
	render(){
		const {
			selected = null,
			hasErrored=false,
			className,
			items = []
		} = this.props;

		const cx = classnames(c.sidebar, className, 'flex-vertical')

		const selected_chat = items.reduce(function(s, x, index){
			if (x.id === selected)
				return index
			return s
		}, -1)

		// console.log('selected chat this time is .. ', selected_chat, selected)

		return (
			<div className={cx}>
				<div className='search-box'>
					<input
						type='search'
						className='search-control'
						placeholder='Search Users/Groups'
						onChange={this.props.onSearchChange}/>
				</div>
				<div className='items-list scroll-y flex-1'>
					{
						hasErrored && <p>Error loading chats</p>
					}
					{
						items.map((x, i)=>
							<ChatSidebarItem
								key={i}
								selected={selected_chat === i}
								onClick={(e)=> this.props.onItemClick(x.id)}
								username={x.username}
								image={x.user_image_url}
								avatar_color={x.user_avatar_color}
								is_online={_.includes(this.props.onlineUsers, x.username)}
								num_unread={x.unread_count}/>
						)
					}
				</div>
			</div>
		)
	}
}

export default Sidebar
