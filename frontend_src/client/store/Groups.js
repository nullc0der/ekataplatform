import request from 'superagent'
const debug = require('debug')('ekata:store:groups')

const DEFAULT_GROUPS = [
	{
		id: 0,
		name: 'Wizards',
		category: "Business",
		image_url: '',
		short_description: 'Lorem ipsum solor di amet, lorem ipsum solor di amet, consectetur adipiscing elit',
		is_subscribed: true,
		is_available: true,
		stats: {
			members: 2000,
			subscribers: 24929,
			active: 39
		}
	},{
		id: 1,
		name: 'Wizards',
		category: "Business",
		image_url: '',
		short_description: 'Lorem ipsum solor di amet, lorem ipsum solor di amet, consectetur adipiscing elit',
		is_subscribed: false,
		is_available: true,
		stats: {
			members: 2000,
			subscribers: 24929,
			active: 39
		}
	},{
		id: 2,
		name: 'Wizards',
		category: "Business",
		image_url: '',
		short_description: 'Lorem ipsum solor di amet, lorem ipsum solor di amet, consectetur adipiscing elit',
		is_subscribed: true,
		is_available: false,
		stats: {
			members: 2000,
			subscribers: 24929,
			active: 39
		}
	},{
		id: 3,
		name: 'Wizards',
		category: "Business",
		image_url: '',
		short_description: 'Lorem ipsum solor di amet, lorem ipsum solor di amet, consectetur adipiscing elit',
		is_subscribed: false,
		is_available: true,
		stats: {
			members: 2000,
			subscribers: 24929,
			active: 39
		}
	},{
		id: 4,
		name: 'Wizards',
		category: "Business",
		image_url: '',
		short_description: 'Lorem ipsum solor di amet, lorem ipsum solor di amet, consectetur adipiscing elit',
		is_subscribed: true,
		is_available: false,
		stats: {
			members: 2000,
			subscribers: 24929,
			active: 39
		}
	}
]

const INITIAL_STATE = {
	groups: [],
	selectedGroup: null
}

const GROUPS_LOAD_SUCCESS = "GROUP_LOAD_SUCCESS"
const groupLoadSuccess = (groups) => ({
	type: GROUPS_LOAD_SUCCESS,
	groups
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

export const actions = {
	loadGroups
}

export default function GroupsReducer(state=INITIAL_STATE, action){
	switch(action.type){
		case GROUPS_LOAD_SUCCESS:
			return {...state, groups: action.groups}
		default:
			return state
	}
}
