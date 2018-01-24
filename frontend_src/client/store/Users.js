import request from 'superagent'

const INITIAL_STATE = {
    users: [],
    onlineUsers: []
}

const USER_FETCH_SUCCESS = 'USER_FETCH_SUCCESS'
const userFetchSuccess = (users) => ({
    type: USER_FETCH_SUCCESS,
    users
})

const ADD_ONLINE_USERS = 'ADD_ONLINE_USERS'
const addOnlineUsers = (users) => ({
    type: ADD_ONLINE_USERS,
    users
})

export const fetchOnlineUsers = (url) => {
    return (dispatch) => {
        request
            .get(url)
            .set('Accept', 'application/json')
            .end((err, res) => {
                if (res.ok) {
                    dispatch(addOnlineUsers(res.body))
                }
            })
    }
}

export const fetchUsers = (url) => {
    return (dispatch) => {
        request
            .get(url)
            .set('Accept', 'application/json')
            .end((err, res) => {
                if (res.ok) {
                    dispatch(userFetchSuccess(res.body))
                }
            })
    }
}

export default function UsersReducer(state=INITIAL_STATE, action) {
    switch(action.type) {
        case USER_FETCH_SUCCESS:
            return {...state, users: action.users}
        case ADD_ONLINE_USERS:
            return {...state, onlineUsers: action.users}
        default:
            return state
    }
}
