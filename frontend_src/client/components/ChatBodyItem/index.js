import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './ChatBodyItem.styl'

import Avatar from 'components/Avatar'

import { Emoji } from 'emoji-mart'
import Linkify from 'react-linkify'

import TimeAgo from 'react-timeago'

class ChatBodyItem extends Component {

	handleSelect = (messageId, shouldSelect) => {
		if (this.props.roomId) {
			this.props.onSelected(this.props.roomId, messageId, shouldSelect)
		} else {
			this.props.onSelected(messageId, shouldSelect)
		}
	}

	renderAttachment = (filetype) => {
		switch (filetype.split('/')[0]) {
			case 'image':
				return (
					<div className={this.props.miniChat ? "img-attachment small": "img-attachment"}>
						<img src={this.props.fileurl} title={this.props.filename} alt={this.props.filename} />
					</div>
				)
			case 'video':
				return (
					<div className={this.props.miniChat ? "video-attachment small": "video-attachment"}>
						<video controls preload="metadata">
							<source src={this.props.fileurl} type={filetype}/>>
						</video>
					</div>
				)
			default:
				return (
					<div className="file-attachment">
						<i className="fa fa-paperclip"></i><a href={this.props.fileurl} target="_blank">{this.props.filename}</a>
					</div>
				)
		}
	}

	render(){
		const {
			className,
			user = {},
			message = '',
			message_id = null,
			selected = false,
			stamp = new Date(),
			left = false,
			fileurl,
			filetype,
			filename
		} = this.props;

		const cx = classnames(c.container, className, 'chat-body-item', {
			'in-left': left
		})

		return (
			<div className={cx}>
				{selected && <i className="material-icons selectmessage">check_circle</i>}
				<a href={user.public_url} style={{color: "transparent"}} className="ui-avatar">
					{
						user.user_image_url ?
							<img className='img-responsive img-chat-avatar rounded' src={user.user_image_url} /> :
							<Avatar name={user.username} bgcolor={user.user_avatar_color} />
					}
				</a>
				<div className='msg' onClick={() => this.handleSelect(this.props.message_id, !left)}>
					{
						filetype ? this.renderAttachment(filetype) : ""
					}
					<Linkify properties={{ target: '_blank' }}>
						{message.split(' ').map((x, i) => {
							return x.startsWith(':') ?
								<Emoji key={i} emoji={x} size={21} tooltip={true} sheetSize={16} /> :
								x + ' '
						})}
					</Linkify>
					<div className='stamp'>
						<TimeAgo date={stamp} minPeriod={10}/>
					</div>
				</div>
			</div>
		)
	}
}

export default withStyles(c)(ChatBodyItem)
