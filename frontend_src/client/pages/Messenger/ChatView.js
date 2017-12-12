import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect} from 'react-redux'

import c from './Messenger.styl'

import ChatBodyItem from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'


class ChatView extends Component {
	closeChatView = ()=> {
		$('.' + c.chatView).toggleClass('is-open')
	}

	sendDemoChat = (e)=> {
		// if (e.keyCode !== 13)
		// 	return

		var val = $('.chat-input-box').val()
		var $chat = $('<div/>', {class: 'chat-body-item'}).text(val)
		$('.chatview-body').append(
			$chat
		)

		$chat.get(0).scrollIntoView();
	}

	render(){
		const {
			className,
			chats
		} = this.props;

		const cx = classnames(c.chatView, className, 'flex-vertical')

		return (
			<div className={cx}>
				<div className='chatview-header flex-horizontal a-center'>
					<div className='text-muted text-session-id'> Session ID: #3949aaudh1 </div>
					<div className='text-username text-center flex-1'> Sharad Kant </div>
					<div className='header-options'>
						<div className='btn btn-default ui-button'>
							<i className='fa fa-ellipsis-v'/>
						</div>
						<div onClick={this.closeChatView} className='btn btn-default btn-chat ui-button mobile-close-chat'>
							<i className='fa fa-remove'/>
						</div>
					</div>
				</div>
				<div className='chatview-body flex-1'>
					{
						chats.map((x, i)=> {
							return <ChatBodyItem
								key={i}
								user='Some User'
								message={x.message}
								stamp={x.stamp}
								left={x.from !== 'me'}/>
						})
					}
				</div>
				<ChatFooter/>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	chats: state.Chat.chats
})
const mapDispatchToProps = (dispatch)=> ({

})

export default connect(mapStateToProps,mapDispatchToProps)(ChatView)
