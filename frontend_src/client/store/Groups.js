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
	groups: DEFAULT_GROUPS.map(x => x),
	selectedGroup: null
}


export const actions = {

}

export default function GroupsReducer(state=INITIAL_STATE, action){
	switch(action.type){
		default:
			return state
	}
}