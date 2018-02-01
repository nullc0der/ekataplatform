import request from 'superagent'

import {actions as commonAction} from './Common'

const INITIAL_STATE = {
	groups: [],
	selectedGroup: null
}

const GROUPS_LOAD_SUCCESS = "GROUP_LOAD_SUCCESS"
const groupLoadSuccess = (groups) => ({
	type: GROUPS_LOAD_SUCCESS,
	groups
})

const SUBSCRIBE_GROUP_SUCCESS = "SUBSUCRIBE_GROUP_SUCCESS"
const subscribeGroupSuccess = (groupID, userName) => ({
	type: SUBSCRIBE_GROUP_SUCCESS,
	groupID,
	userName
})

const UNSUBSCRIBE_GROUP_SUCCESS = "UNSUBSUCRIBE_GROUP_SUCCESS"
const unSubscribeGroupSuccess = (groupID, userName) => ({
	type: UNSUBSCRIBE_GROUP_SUCCESS,
	groupID,
	userName
})

const GROUP_CREATED = 'GROUP_CREATED'
const groupCreated = (group) => ({
	type: GROUP_CREATED,
	group
})

const JOIN_REQUEST_SENT = 'JOIN_REQUEST_SENT'
const joinRequestSent = (groupID) => ({
	type: JOIN_REQUEST_SENT,
	groupID
})

const JOIN_REQUEST_CANCELED = 'JOIN_REQUEST_CANCELED'
const joinRequestCanceled = (groupID) => ({
	type: JOIN_REQUEST_CANCELED,
	groupID
})

const LEFT_GROUP = 'LEFT_GROUP'
const leftGroup = (groupID) => ({
	type: LEFT_GROUP,
	groupID
})

const loadGroups = (url) => {
	return (dispatch) => {
		request
			.get(url)
			.end((err, res) => {
				if (res.ok) {
					dispatch(groupLoadSuccess(res.body))
				}
			})
	}
}

const subscribeGroup = (url) => {
	return (dispatch) => {
		request
			.post(url)
			.set('X-CSRFToken', window.django.csrf)
			.send({'subscribe': true})
			.end((err, res) => {
				if (res.ok) {
					if (res.body.subscribed) {
						dispatch(subscribeGroupSuccess(res.body.group_id, res.body.username))
						dispatch(commonAction.addNotification({
							message: 'Subscribed successfully',
							level: 'success'
						}))
					} else {
						dispatch(commonAction.addNotification({
							message: 'Error subscribing, please try later',
							level: 'error'
						}))
					}
				}
			})
	}
}

const unSubscribeGroup = (url) => {
	return (dispatch) => {
		request
			.post(url)
			.set('X-CSRFToken', window.django.csrf)
			.send({ 'subscribe': false })
			.end((err, res) => {
				if (res.ok) {
					if (!res.body.subscribed) {
						dispatch(unSubscribeGroupSuccess(res.body.group_id, res.body.username))
						dispatch(commonAction.addNotification({
							message: 'Unsubscribed successfully',
							level: 'success'
						}))
					} else {
						dispatch(commonAction.addNotification({
							message: 'Error unsubscribing, please try later',
							level: 'error'
						}))
					}
				}
			})
	}
}

const joinGroup = (groupID, type) => {
	const url = `/api/groups/join/${groupID}/`
	return (dispatch) => {
		request
			.post(url)
			.set('X-CSRFToken', window.django.csrf)
			.send({ 'type': type })
			.end((err, res) => {
				if (res.ok) {
					if (!res.body.success) {
						dispatch(commonAction.addNotification({
							message: res.body.message || 'Error!! please try later',
							level: 'error'
						}))
					} else {
						if (res.body.type === 'leave') {
							dispatch(leftGroup(res.body.group_id))
						}
						if (res.body.type === 'cancel') {
							dispatch(joinRequestCanceled(res.body.group_id))
						}
						if (res.body.type === 'join') {
							dispatch(joinRequestSent(res.body.group_id))
						}
					}
				}
			})
	}
}

export const actions = {
	loadGroups,
	subscribeGroup,
	unSubscribeGroup,
	groupCreated,
	joinGroup
}

export default function GroupsReducer(state=INITIAL_STATE, action){
	switch(action.type){
		case GROUPS_LOAD_SUCCESS:
			return {...state, groups: action.groups}
		case SUBSCRIBE_GROUP_SUCCESS:
			return {...state, groups: state.groups.map(x => {
				return x.id === action.groupID ? {...x, subscribers:x.subscribers.concat(action.userName)} : x
			})}
		case UNSUBSCRIBE_GROUP_SUCCESS:
			return {...state, groups: state.groups.map(x => {
				return x.id === action.groupID ? {...x, subscribers:x.subscribers.filter(x=>x!==action.userName)}: x
			})}
		case GROUP_CREATED:
			return {...state, groups: [...state.groups, action.group]}
		case JOIN_REQUEST_SENT:
			return {
				...state, groups: state.groups.map(x => {
					return x.id === action.groupID ? { ...x, joinrequest_sent: true } : x
				})
			}
		case JOIN_REQUEST_CANCELED:
			return {
				...state, groups: state.groups.map(x => {
					return x.id === action.groupID ? { ...x, joinrequest_sent: false } : x
				})
			}
		case LEFT_GROUP:
			return {
				...state, groups: state.groups.map(x => {
					return x.id === action.groupID ? { ...x, members: x.members.filter(x => x !== window.django.user.username) } : x
				})
			}
		default:
			return state
	}
}
