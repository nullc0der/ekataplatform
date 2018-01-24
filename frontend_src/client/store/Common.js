const debug = require('debug')('ekata:store:common')

const INITIAL_STATE = {
	breadcrumbs: {
		title: 'Home',
		links: [{href: '/', text: 'Home'}]
	},
	showHeaders: true,
	notification: {
		message: '',
		level: ''
	},
	subHeaderSearchString: '',
	subHeaderFilters: []
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

const ADD_NOTIFICATION = 'ADD_NOTIFICATION'
const addNotification = (notification) => ({
	type: ADD_NOTIFICATION,
	notification
})

const CHANGE_SUBHEADER_SEARCHSTRING = 'CHANGE_SUBHEADER_SEARCHSTRING'
const changeSubHeaderSearchString = (searchString) => ({
	type: CHANGE_SUBHEADER_SEARCHSTRING,
	searchString
})

const CHANGE_SUBHEADER_FILTERS = 'CHANGE_SUBHEADER_FILTERS'
const changeSubHeaderFilters = (filters) => ({
	type: CHANGE_SUBHEADER_FILTERS,
	filters
})

export const actions = {
	setBreadCrumbs,
	updateHeaderVisibility,
	addNotification,
	changeSubHeaderSearchString,
	changeSubHeaderFilters
}

export default function CommonReducer(state = INITIAL_STATE, action){
	switch(action.type){
		case SET_BREADCRUMBS:
			return {...state, breadcrumbs: {title: action.title, links: action.links}}
		case UPDATE_HEADER_VISIBILITY:
			return {...state, showHeaders: action.showHeaders}
		case ADD_NOTIFICATION:
			return {...state, notification: action.notification}
		case CHANGE_SUBHEADER_SEARCHSTRING:
			return {...state, subHeaderSearchString: action.searchString}
		case CHANGE_SUBHEADER_FILTERS:
			return {...state, subHeaderFilters: action.filters}
		default:
			return state
	}
}
