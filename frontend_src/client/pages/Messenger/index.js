import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Messenger.styl'

import Sidebar  from './Sidebar'
import ChatView from './ChatView'

import SAMPLE_CHATS from './sample-chats'
import SAMPLE_DETAILED_CHAT from './sample-detailed-chat'

class Messenger extends Component {
	state = {
		selected: 0,
		sidebar_chats: [],
		active_chat: []
	}

	componentDidMount = ()=> {
		this.getSidebarChats()
			.then(sidebar_chats => {
				this.setState({sidebar_chats})
				return Promise.resolve(sidebar_chats)
			}).then(chats=>
				this.getChatDetails(chats[0].id)
			)
	}

	getSidebarChats = ()=> {
		return Promise.resolve(SAMPLE_CHATS)
	}

	getChatDetails = (chatId)=> {
		return Promise.resolve(SAMPLE_DETAILED_CHAT)
	}

	onSidebarChatSelect = (id)=> {
		console.log('clicked something: ', id)
		this.getChatDetails(id)
			.then(active_chat => {
				this.setState({active_chat})
			})
		$('.' + c.chatView).toggleClass('is-open')
	}


	render(){
		const {
			className
		} = this.props;

		const cx = classnames(c.container, className, 'flex-horizontal', 'a-stretch', 'flex-1')

		return (
			<div className={cx}>
				<Sidebar
					selected={this.state.selected}
					onItemClick={this.onSidebarChatSelect}
					items={this.state.sidebar_chats}/>
				<ChatView
					/>
			</div>
		)
	}
}

export default withStyles(c)(Messenger)
