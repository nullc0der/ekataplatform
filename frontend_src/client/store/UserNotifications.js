import request from 'superagent'


const INITIAL_STATE = {
    notifications: []
}

const NOTIFICATION_FETCH_SUCCESS = 'NOTIFICATION_FETCH_SUCCESS'
const notificationFetchSuccess = (notifications) => ({
    type: NOTIFICATION_FETCH_SUCCESS,
    notifications
})

const fetchNotifications = (url) => {
    return (dispatch) => {
        request
            .get(url)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(notificationFetchSuccess(res.body))
                }
            })
    }
}

export const actions = {
    fetchNotifications
}

export default function UserNotificationsReducer(state=INITIAL_STATE, action) {
    switch(action.type) {
        case NOTIFICATION_FETCH_SUCCESS:
            return {
                ...state, notifications: action.notifications
            }
        default:
            return state
    }
}
