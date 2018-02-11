import request from 'superagent'

const MEMBER_GROUPS = [
	{id: 101, name: 'Subscriber', icon: 'face'},
	{id: 102, name: 'Member', icon: 'group_add'},
	{id: 103, name: 'Owner', icon: 'local_library'},
	{id: 104, name: 'Administrator', icon: 'spellcheck'},
	{id: 105, name: 'Moderator', icon: 'verified_user'},
	{id: 106, name: 'Staff', icon: 'touch_app'},
	{id: 107, name: 'Ban', icon: 'remove_circle_outline'},
	{id: 108, name: 'Block', icon: 'block'},
]


const INITIAL_STATE = {
	list: [],
	groups_list: MEMBER_GROUPS.map(x => x),
	joinRequests: [],
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

const JOIN_REQUEST_FETCH_SUCCESS = 'JOIN_REQUEST_FETCH_SUCCESS'
const joinRequestFetchSuccess = (joinRequests) => ({
	type: JOIN_REQUEST_FETCH_SUCCESS,
	joinRequests
})


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

const DELETE_JOIN_REQUEST = 'DELETE_JOIN_REQUEST'
const deleteJoinRequest = (requestID) => ({
	type: DELETE_JOIN_REQUEST,
	requestID
})

const RECEIVED_JOIN_REQUEST_ON_WEBSOCKET = 'RECEIVED_JOIN_REQUEST_ON_WEBSOCKET'
const receivedJoinRequestOnWebsocket = (joinRequest) => ({
	type: RECEIVED_JOIN_REQUEST_ON_WEBSOCKET,
	joinRequest
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

const getJoinRequests = (url) => {
	return (dispatch) => {
		request
			.get(url)
			.end((err, res) => {
				if (res.ok) {
					dispatch(joinRequestFetchSuccess(res.body))
				}
			})
	}
}

const acceptDenyJoinRequest = (url, requestID, accepted) => {
	return (dispatch) => {
		request
			.post(url)
			.set('X-CSRFToken', window.django.csrf)
			.send({'accept': accepted})
			.end((err, res) => {
				if (res.ok) {
					if (res.body.request_id) {
						dispatch(deleteJoinRequest(res.body.request_id))
					} else {
						dispatch(joinRequestAccepted(res.body))
						dispatch(deleteJoinRequest(requestID))
					}
				}	
			})
	}
}

export const actions = {
	toggleSubscribedGroup,
	getGroupMembers,
	getJoinRequests,
	acceptDenyJoinRequest,
	receivedJoinRequestOnWebsocket
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
		case JOIN_REQUEST_FETCH_SUCCESS:
			return {
				...state, joinRequests: action.joinRequests
			}
		case JOIN_REQUEST_ACCEPTED:
			return {
				...state, list: [...state.list, action.member]
			}
		case DELETE_JOIN_REQUEST:
			return {
				...state, joinRequests: state.joinRequests.filter(
					x => x.id !== action.requestID
				)
			}
		case RECEIVED_JOIN_REQUEST_ON_WEBSOCKET:
			return {
				...state, joinRequests: [...state.joinRequests, action.joinRequest]
			}
		case CHANGE_ACCESS_DENIED:
			return {
				...state, accessDenied: action.access
			}
		default:
			return state
	}
}
