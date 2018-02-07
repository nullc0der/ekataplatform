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

	state = {
		list: []
	}

	componentDidMount = () => {
		const id = this.props.groupID
		this.props.getMembers(`/api/groups/${id}/members/`)
	}

	componentDidUpdate = (prevProps) => {
		if (
			prevProps.list !== this.props.list ||
			prevProps.searchString !== this.props.searchString ||
			prevProps.filters !== this.props.filters
		) {
			this.setUsers(
				this.props.list,
				this.props.searchString,
				this.props.filters
			)
		}
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

	setUsers = (list, searchString='', filters=[]) => {
		let finalList = list.filter(
			x => x.user.username.toLowerCase().startsWith(searchString.toLowerCase()))
		let filteredItems = []
		for (const filter of filters) {
			switch(filter) {
				case 'owners':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 103)))
					break
				case 'admins':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 104)))
					break
				case 'moderators':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 105)))
					break
				case 'members':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 102)))
					break
				case 'subscribers':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 101)))
					break
				case 'banned':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 107)))
					break
			}
		}
		if (filteredItems.length) {
			finalList = _.union(...filteredItems)
		}
		this.setState({
			list: finalList
		})
	}

	render(){
		const {
			className
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
						this.state.list.map(this.renderOneMember)
					}
				</div>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	list: state.Members.list,
	groups: state.Members.groups_list,
	onlineUsers: state.Users.onlineUsers,
	searchString: state.Common.subHeaderSearchString,
	filters: state.Common.subHeaderFilters
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
