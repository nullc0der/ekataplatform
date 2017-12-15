import request from 'superagent'
const debug = require('debug')('ekata:store:chatrooms')

const INITIAL_STATE = {
    rooms: [],
    areLoading: false,
    hasErrored: false,
    selected: 0,
    searchText: ''
}

const ROOMS_ARE_LOADING = 'ROOMS_ARE_LOADING'
const roomsAreLoading = (areLoading) => ({
    type: ROOMS_ARE_LOADING,
    areLoading
})

const ROOMS_HAS_ERRORED = 'ROOMS_HAS_ERRORED'
const roomsHasErrored = (hasErrored) => ({
    type: ROOMS_HAS_ERRORED,
    hasErrored
})

const ROOMS_FETCH_DATA_SUCCESS = 'ROOMS_FETCH_DATA_SUCCESS'
const roomsFetchDataSuccess = (rooms) => ({
    type: ROOMS_FETCH_DATA_SUCCESS,
    rooms
})

const ROOM_SELECTED = 'ROOM_SELECTED'
export const roomSelected = (selected) => ({
    type: ROOM_SELECTED,
    selected
})

const SEARCH_TEXT_CHANGED = 'SEARCH_TEXT_CHANGED'
export const searchTextChanged = (searchText) => ({
    type: SEARCH_TEXT_CHANGED,
    searchText
})

export const roomsFetchData = (url) => { 
    return (dispatch) => {
        dispatch(roomsAreLoading(true))
        request
            .get(url)
            .set('Accept', 'application/json')
            .end((err, res) => {
                if (err || !res.ok) {
                    dispatch(roomsHasErrored(true))
                } else {
                    dispatch(roomsFetchDataSuccess(res.body))
                    dispatch(roomSelected(res.body[0].id))
                }
            })
    }
}

export default function ChatRoomsReducer(state=INITIAL_STATE, action) {
    switch(action.type) {
        case ROOMS_ARE_LOADING:
            return {...state, areLoading: action.areLoading}
        case ROOMS_HAS_ERRORED:
            return {...state, hasErrored: action.hasErrored}
        case ROOMS_FETCH_DATA_SUCCESS:
            return {...state, rooms: action.rooms}
        case ROOM_SELECTED:
            return {...state, selected: action.selected}
        case SEARCH_TEXT_CHANGED:
            return {...state, searchText: action.searchText}
        default:
            return state
    }
}
