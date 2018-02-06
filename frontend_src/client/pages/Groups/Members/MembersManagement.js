import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Members.styl'
import _ from 'lodash'

import MemberItem from './MemberItem'

import {actions as memberActions} from 'store/Members'

class MembersManagement extends Component {

	componentDidMount = () => {
		const id = this.props.groupID
		this.props.getMembers(`/api/groups/${id}/members/`)
	}

	toggleSubscribedGroup = (memberID, subscribedGroups, toggledGroup) => {
		const id = this.props.groupID
		this.props.toggleSubscribedGroup(
			`/api/groups/${id}/members/${memberID}/changerole/`,
			subscribedGroups,
			toggledGroup
		)
	}

	renderOneMember = (member, i)=> {
		const {groups} = this.props;
		return <MemberItem
			key={i}
			groups={groups}
			memberId={member.user.id}
			fullName={member.user.fullname}
			userName={member.user.username}
			isOnline={member.user.is_online}
			avatarUrl={member.user.user_image_url}
			avatarColor={member.user.user_avatar_color}
			publicURL={member.user.public_url}
			isStaff={member.user.is_staff}
			toggleSubscribedGroup={this.toggleSubscribedGroup}
			subscribed_groups={member.subscribed_groups}
			isOnline={_.includes(this.props.onlineUsers, member.user.username)}/>
	}

	render(){
		const {
			className,
			list = []
		} = this.props;

		const cx = classnames(className, 'flex-vertical')

		return (
			<div className={cx}>
				<div className='panel-header'>
					<div className='header-inner'>
						<h4> Member Management </h4>
					</div>
				</div>
				<div className='members-list'>
					{
						list.map(this.renderOneMember)
					}
				</div>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	list: state.Members.list,
	groups: state.Members.groups_list,
	onlineUsers: state.Users.onlineUsers
})

const mapDispatchToProps = (dispatch)=> ({
	toggleSubscribedGroup: (url, subscribedGroups, toggledGroup) => {
		dispatch(memberActions.toggleSubscribedGroup(url, subscribedGroups, toggledGroup))
	},
	getMembers: (url) => {
		dispatch(memberActions.getGroupMembers(url))
	}
})

export default connect(mapStateToProps,mapDispatchToProps)(MembersManagement)
