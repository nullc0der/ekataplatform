const debug = require('debug')('ekata:store:common')

const INITIAL_STATE = {
	breadcrumbs: {
		title: 'Home',
		links: [{href: '/', text: 'Home'}]
	},
	showHeaders: true
}

const SET_BREADCRUMBS = 'SET_BREADCRUMBS'
const setBreadCrumbs = (data)=> ({
	type: SET_BREADCRUMBS,
	title: data.title,
	links: data.links
})

const UPDATE_HEADER_VISIBILITY = 'UPDATE_HEADER_VISIBILITY'
const updateHeaderVisibility = (showHeaders) => ({
	type: UPDATE_HEADER_VISIBILITY,
	showHeaders
})

export const actions = {
	setBreadCrumbs,
	updateHeaderVisibility
}

export default function CommonReducer(state = INITIAL_STATE, action){
	switch(action.type){
		case SET_BREADCRUMBS:
			return {...state, breadcrumbs: {title: action.title, links: action.links}}
		case UPDATE_HEADER_VISIBILITY:
			return {...state, showHeaders: action.showHeaders}
		default:
			return state
	}
}
