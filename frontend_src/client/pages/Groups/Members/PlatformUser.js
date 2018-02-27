import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import Avatar  from 'components/Avatar'

class MemberItem extends Component {

	render(){
		const {
			className,
			inviteUser,
			userId,
			userName = '',
			fullName = '',
			avatarUrl = '',
			avatarColor = '',
			publicURL = '',
			isInvited = false
		} = this.props;

		const cx = classnames(className, 'ui-member-item', 'flex-horizontal j-between')

		return (
			<div className={cx}>
				<div className='flex-horizontal a-center flex-1'>
					<div className='in-left flex-horizontal a-center'>
						<a href={publicURL}>
							{
								avatarUrl ?
									<img className='avatar-image rounded' src={avatarUrl} /> :
									<Avatar className='avatar-image' name={fullName || userName} bgcolor={avatarColor} />
							}
						</a>
						<div className='details'>
							<div className='name'> {fullName || userName} </div>
						</div>
					</div>
					<div className='in-right flex-horizontal flex-1'>
						<div
							className='subscribed-groups flex-horizontal-reverse a-center'>
							<i className={`fa fa-user-plus invitebtn ${!isInvited ? 'not-invited': ''}`} onClick={(e) => inviteUser(e, userId)}></i>
						</div>
					</div>
				</div>
			</div>
		)
	}
}

export default MemberItem
