import {Component} from 'react'
import classnames  from 'classnames'
import {connect}   from 'react-redux'

import moment from 'moment'

import ChatBodyItem  from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'

import c from './HeaderMiniChat.styl'

import {actions as chatActions} from 'store/Chat'

import {generateRandomDate, getOnlineStatus} from 'utils/common'

class MiniChat extends Component {
	state = {
		chats: [],
		isLoading: true,
		hasError: false
	}

	closeChat = (chat)=> (e)=> {
		this.props.closeMiniChat(chat.id)
	}

	toggleMinimise = (e)=> {
		var $btn  = $(e.currentTarget)
		var $chat = $btn.parents('.mini-chat')

		if ( $chat.hasClass('is-minimized') ){
			$btn.find('.fa').removeClass('fa-window-maximize').addClass('fa-window-minimize')
			$chat.removeClass('is-minimized')
		} else {
			$btn.find('.fa').removeClass('fa-window-minimize').addClass('fa-window-maximize')
			$chat.addClass('is-minimized')
		}

		console.log('will min', $chat.get(0))
	}

	renderOneChat = (chat, i)=> {
		const cx = classnames('chat-header', 'flex-horizontal', 'a-center', 'j-between', getOnlineStatus(chat.status))
		return <div key={i} className='mini-chat flex-vertical'>
			<div className={cx}>
				<div className='username'> {chat.user} </div>
				<div className='chat-options'>
					<div
						onClick={this.toggleMinimise}
						className='btn btn-default ui-button'>
						<i className='fa fa-window-minimize'/>
					</div>
					<div
						onClick={this.closeChat(chat)}
						className='btn btn-default ui-button'>
						<i className='fa fa-remove'/>
					</div>
				</div>
			</div>
			<div className='chat-body flex-1'>
				{
					chat.messages.map((x,i)=> {
						return <ChatBodyItem
							key={i}
							user={chat.user}
							message={x.message}
							stamp={x.stamp}
							left={x.from !== 'me'}/>
					})
				}
			</div>
			<ChatFooter small={true}/>
		</div>
	}

	render(){
		const {className, chats = []} = this.props;
		const cx = classnames(c.miniChatHolder, 'mini-chat-holder', 'flex-horizontal')
		return (
			<div className={cx}>
				{
					chats.map(this.renderOneChat)
				}
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	chats: state.Chat.minichats
})

const mapDispatchToProps = (dispatch)=> ({
	closeMiniChat(id){
		return dispatch(chatActions.closeMiniChat(id))
	}
})

export default connect(mapStateToProps,mapDispatchToProps)(MiniChat)