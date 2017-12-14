import request from 'superagent'
const debug = require('debug')('ekata:store:chatrooms')

const INITIAL_STATE = {
    rooms: [],
    areLoading: false,
    hasErrored: false
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

const roomsFetchData = (url) => { 
    (dispatch) => {
        dispatch(roomsAreLoading(true))
        request
            .get(url)
            .set('Accept', 'application/json')
            .end((err, res) => {
                if (err || !res.ok) {
                    dispatch(roomsHasErrored(true))
                } else {
                    dispatch(roomsFetchDataSuccess(res.body))
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
        default:
            return state
    }
}
