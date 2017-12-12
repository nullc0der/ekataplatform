import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import c from './Messenger.styl'

import ChatSidebarItem from './ChatSidebarItem'

class Sidebar extends Component {
	render(){
		const {
			selected = null,
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
						placeholder='Search Users/Groups'/>
				</div>
				<div className='items-list scroll-y flex-1'>
					{
						items.map((x, i)=>
							<ChatSidebarItem
								key={i}
								selected={selected_chat === i}
								onClick={(e)=> this.props.onItemClick(x.id)}
								username={x.username}
								image={x.image}
								status={x.status}
								num_unread={x.num_unread}/>
						)
					}
				</div>
			</div>
		)
	}
}

export default Sidebar
