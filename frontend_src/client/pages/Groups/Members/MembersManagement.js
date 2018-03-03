import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import request from 'superagent'
import _ from 'lodash'
import withRouter from 'react-router/lib/withRouter'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Members.styl'
import MemberItem from './MemberItem'
import PlatformUser from './PlatformUser'

import {actions as memberActions} from 'store/Members'
import {actions as groupActions} from 'store/Groups'
import {actions as commonActions} from 'store/Common'

class MembersManagement extends Component {

	state = {
		list: [],
		platformUserList: []
	}

	componentDidMount = () => {
		const id = this.props.groupID
		this.props.getMembers(`/api/groups/${id}/members/`)
		this.props.changeLastGroup(id)
	}

	componentDidUpdate = (prevProps) => {
		if (this.props.accessDenied) {
			this.props.router.push('/error/403')
		}
		if (
			prevProps.list !== this.props.list ||
			prevProps.onlineUsers !== this.props.onlineUsers ||
			prevProps.searchString !== this.props.searchString ||
			prevProps.filters !== this.props.filters
		) {
			this.setUsers(
				this.props.list,
				this.props.onlineUsers,
				this.props.searchString,
				this.props.filters
			)
		}
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
			subscribed_groups={member.subscribed_groups}
			isOnline={member.user.is_online}/>
	}

	renderOnePlatformuser = (user, i) => {
		return <PlatformUser
			key={i}
			userId={user.id}
			fullName={user.fullname}
			userName={user.username}
			avatarUrl={user.user_image_url}
			avatarColor={user.user_avatar_color}
			publicURL={user.public_url}
			isInvited={user.is_invited}
			inviteUser={this.inviteUser} />
	}

	getEkataMembers = (searchString) => {
		if(searchString.length >= 3) {
			request
				.get(`/api/groups/${this.props.groupID}/invitemember/?query=${searchString}`)
				.end((err, res) => {
					if (res.ok) {
						this.setState({
							platformUserList: res.body
						})
					}
				})
		}
	}

	setUsers = (list, onlineUsers, searchString='', filters=[]) => {
		if (filters.indexOf('Ekata Members') !== -1 && searchString) {
			this.getEkataMembers(searchString)
		} else {
			this.setState({
				platformUserList: []
			})
		}
		let finalList = list.map(
			x => _.includes(onlineUsers, x.user.username)
			? {...x, user: {...x.user, is_online: true}}
			: {...x, user: {...x.user, is_online: false}}
		)
		finalList = finalList.filter(
			x => x.user.username.toLowerCase().startsWith(searchString.toLowerCase()))
		if (filters.indexOf('online') !== -1) {
			finalList = finalList.filter(x=>x.user.is_online)
		}
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
				case 'staffs':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 106)))
					break
				case 'moderators':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 105)))
					break
				case 'members':
					filteredItems.push(
						finalList.filter(x => _.includes(x.subscribed_groups, 102)))
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

	inviteUser = (e, id) => {
		request
			.post(`/api/groups/${this.props.groupID}/invitemember/`)
			.set('X-CSRFToken', window.django.csrf)
			.send({ 'user_id': id })
			.end((err, res) => {
				if (res.ok) {
					this.props.addNotification({
						'message': 'User invited',
						'level': 'success'
					})
				}
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
						<h4> Members </h4>
					</div>
				</div>
				<div className='members-list'>
					{
						this.state.platformUserList.map(this.renderOnePlatformuser)
					}
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
	accessDenied: state.Members.accessDenied,
	onlineUsers: state.Users.onlineUsers,
	searchString: state.Common.subHeaderSearchString,
	filters: state.Common.subHeaderFilters,
	joinStatus: state.Groups.viewingGroupJoinStatus,
	permissionSet: state.Groups.userPermissionSetForViewingGroup
})

const mapDispatchToProps = (dispatch)=> ({
	getMembers: (url) => {
		dispatch(memberActions.getGroupMembers(url))
	},
	changeLastGroup: (id) => {
		dispatch(groupActions.changeLastGroup(id))
	},
	addNotification: (notification) => {
		dispatch(commonActions.addNotification(notification))
	}
})

export default withRouter(
	connect(mapStateToProps,mapDispatchToProps)(MembersManagement))
