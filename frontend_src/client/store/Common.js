const debug = require('debug')('ekata:store:common')

const INITIAL_STATE = {
	breadcrumbs: {
		title: 'Home',
		links: [{href: '/', text: 'Home'}]
	}
}

const SET_BREADCRUMBS = 'SET_BREADCRUMBS'
const setBreadCrumbs = (data)=> ({
	type: SET_BREADCRUMBS,
	title: data.title,
	links: data.links
})

export const actions = {
	setBreadCrumbs
}

export default function CommonReducer(state = INITIAL_STATE, action){
	switch(action.type){
		case SET_BREADCRUMBS:
			return {...state, breadcrumbs: {title: action.title, links: action.links}}
		default:
			return state
	}
}