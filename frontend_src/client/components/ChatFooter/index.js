import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './ChatFooter.styl'

class ChatFooter extends Component {
	onChatSend = (e)=> {
		const msg = e.target.value;
		console.log('sending chat: ', msg)
	}
	render(){
		const {
			className,
			small = false
		} = this.props;

		const cx = classnames(
			c.container, className, 'chatview-footer ui-chat-footer flex-horizontal a-stretch',{
				'is-small': small
			}
		)

		return (
			<div className={cx}>
				<div className='btn btn-default ui-button btn-attachment'>
					<i className='fa fa-paperclip'/>
				</div>
				<div className='btn btn-default ui-button btn-camera'>
					<i className='fa fa-camera-retro'/>
				</div>
				<div className='chat-input-wrap flex-1 flex-horizontal a-stretch'>
					<input
						className='chat-input-box'
						type='text'
						placeholder='Type here...'
						onInput={this.onChatSend}/>
					<div className='btn btn-default ui-button chat-input-btn'>
						<i className='fa fa-paper-plane'/>
					</div>
				</div>
				<div className='btn btn-default ui-button'>
					<i className='fa fa-smile-o'/>
				</div>
			</div>
		)
	}
}

export default withStyles(c)(ChatFooter)
