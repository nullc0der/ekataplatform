import request from 'superagent'
import { actions as groupMemberNotificationActions } from './GroupMemberNotification'

const MEMBER_GROUPS = [
	{id: 101, name: 'Subscriber', icon: { type: 'material', name: 'face'}},
	{ id: 102, name: 'Member', icon: { type: 'fa', name: 'users' }},
	{ id: 103, name: 'Owner', icon: { type: 'material', name: 'local_library' }},
	{ id: 104, name: 'Administrator', icon: { type: 'material', name: 'spellcheck' }},
	{ id: 105, name: 'Moderator', icon: { type: 'material', name: 'verified_user' }},
	{ id: 106, name: 'Staff', icon: { type: 'material', name: 'touch_app' }},
	{ id: 107, name: 'Ban', icon: { type: 'material', name: 'remove_circle_outline' }},
	{ id: 108, name: 'Block', icon: { type: 'material', name: 'block' }},
]


const INITIAL_STATE = {
	list: [],
	groups_list: MEMBER_GROUPS.map(x => x),
	accessDenied: false
}

const TOGGLE_SUBSCRIBED_GROUP_SUCCESS = 'TOGGLE_SUBSCRIBED_GROUP_SUCCESS'
const toggleSubscribedGroupSuccess = (memberId, subscribedGroups)=> {
	return {
		type: TOGGLE_SUBSCRIBED_GROUP_SUCCESS,
		memberId,
		subscribedGroups
	}
}


const GROUP_MEMBER_FETCH_SUCCESS = 'GROUP_MEMBER_FETCH_SUCCESS'
const groupMemberFetchSuccess = (members) => ({
	type: GROUP_MEMBER_FETCH_SUCCESS,
	members
})


const JOIN_REQUEST_ACCEPTED = 'JOIN_REQUEST_ACCEPTED'
const joinRequestAccepted = (member) => ({
	type: JOIN_REQUEST_ACCEPTED,
	member
})


const CHANGE_ACCESS_DENIED = 'CHANGE_ACCESS_DENIED'
const changeAccessDenied = (access) => ({
	type: CHANGE_ACCESS_DENIED,
	access
})


const toggleSubscribedGroup = (url, subscribedGroups, toggledGroup) => {
	subscribedGroups = subscribedGroups.indexOf(toggledGroup.id) !== -1
		? subscribedGroups.filter(x => x !== toggledGroup.id)
		: [...subscribedGroups, toggledGroup.id]
	return (dispatch) => {
		request
			.post(url)
			.set('X-CSRFToken', window.django.csrf)
			.send({'subscribed_groups': subscribedGroups})
			.end((err, res) => {
				if (res.ok) {
					dispatch(toggleSubscribedGroupSuccess(
						res.body.member_id,
						res.body.subscribed_groups
					))
				}
			})
	}
}

const getGroupMembers = (url) => {
	return (dispatch) => {
		dispatch(changeAccessDenied(false))
		request
			.get(url)
			.end((err, res) => {
				if (res.ok) {
					dispatch(groupMemberFetchSuccess(res.body))	
				}
				if (err && err.status === 403) {
					dispatch(changeAccessDenied(true))
				}
			})
	}
}


const acceptDenyJoinRequest = (url, notificationID, accepted) => {
	return (dispatch) => {
		request
			.post(url)
			.set('X-CSRFToken', window.django.csrf)
			.send({'accept': accepted})
			.end((err, res) => {
				if (res.ok) {
					if (res.body.request_id) {
						dispatch(groupMemberNotificationActions.removeMemberNotification(notificationID))
					} else {
						dispatch(joinRequestAccepted(res.body))
						dispatch(groupMemberNotificationActions.removeMemberNotification(notificationID))
					}
				}	
			})
	}
}

export const actions = {
	toggleSubscribedGroup,
	getGroupMembers,
	acceptDenyJoinRequest
}

export default function MembersReducer(state = INITIAL_STATE, action){
	switch(action.type){
		case GROUP_MEMBER_FETCH_SUCCESS:
			return {...state, list: action.members}
		case TOGGLE_SUBSCRIBED_GROUP_SUCCESS:
			return {
				...state,
				list: state.list.map(x => {
					if (x.user.id === action.memberId){
						x.subscribed_groups = action.subscribedGroups
					}
					return x
				})
			}
		case JOIN_REQUEST_ACCEPTED:
			return {
				...state, list: [...state.list, action.member]
			}
		case CHANGE_ACCESS_DENIED:
			return {
				...state, accessDenied: action.access
			}
		default:
			return state
	}
}
