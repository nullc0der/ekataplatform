import request from 'superagent'

const DEFAULT_LIST = [
	{
		"status": "Available",
		"name": "Simone Swanson",
		"id": 0,
		"subscribed_groups": [102, 103]
	},
	{
		"status": "Offline",
		"name": "Catherine Mckenzie",
		"id": 1,
		"subscribed_groups": []
	},
	{
		"status": "Available",
		"name": "Hinton Wade",
		"id": 2,
		"subscribed_groups": [103, 105, 106]
	},
	{
		"status": "Offline",
		"name": "Tessa Rasmussen",
		"id": 3,
		"subscribed_groups": []
	},
	{
		"status": "Offline",
		"name": "Charlotte Slater",
		"id": 4,
		"subscribed_groups": [104, 107, 108]
	},
	{
		"status": "Away",
		"name": "Moses Mills",
		"id": 5,
		"subscribed_groups": [102, 106, 108]
	},
	{
		"status": "Away",
		"name": "Ila Stein",
		"id": 6,
		"subscribed_groups": []
	},
	{
		"status": "Offline",
		"name": "Russo West",
		"id": 7,
		"subscribed_groups": []
	},
	{
		"status": "Offline",
		"name": "Geraldine Carlson",
		"id": 8,
		"subscribed_groups": []
	}
]


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
	groups_list: MEMBER_GROUPS.map(x => x)
}

const TOGGLE_SUBSCRIBED_GROUP = 'TOGGLE_SUBSCRIBED_GROUP'
const toggleSubscribedGroup = (memberId, group)=> {
	return {
		type: TOGGLE_SUBSCRIBED_GROUP,
		memberId,
		group
	}
}

const GROUP_MEMBER_FETCH_SUCCESS = 'GROUP_MEMBER_FETCH_SUCCESS'
const groupMemberFetchSuccess = (members) => ({
	type: GROUP_MEMBER_FETCH_SUCCESS,
	members
})

const getGroupMembers = (url) => {
	return (dispatch) => {
		request
			.get(url)
			.end((err, res) => {
				if (res.ok) {
					dispatch(groupMemberFetchSuccess(res.body))	
				}
			})
	}
}

export const actions = {
	toggleSubscribedGroup,
	getGroupMembers
}

export default function MembersReducer(state = INITIAL_STATE, action){
	switch(action.type){
		case GROUP_MEMBER_FETCH_SUCCESS:
			return {...state, list: action.members}
		case TOGGLE_SUBSCRIBED_GROUP:
			return {
				...state,
				list: state.list.map(x => {
					if (x.id === action.memberId){
						x.subscribed_groups = x.subscribed_groups.indexOf(action.group.id) === -1
							? [...x.subscribed_groups, action.group.id]
							: x.subscribed_groups.filter(x => x !== action.group.id)
					}
					return x
				})
			}
		default:
			return state
	}
}
