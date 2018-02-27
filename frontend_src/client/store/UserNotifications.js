import request from 'superagent'


const INITIAL_STATE = {
    notifications: []
}

const NOTIFICATION_FETCH_SUCCESS = 'NOTIFICATION_FETCH_SUCCESS'
const notificationFetchSuccess = (notifications) => ({
    type: NOTIFICATION_FETCH_SUCCESS,
    notifications
})

const REMOVE_NOTIFICATION = 'REMOVE_NOTIFICATION'
const removeNotification = (id) => ({
    type: REMOVE_NOTIFICATION,
    id
})

const RECEIVED_USER_WEBSOCKET_NOTIFICATION = 'RECEIVED_USER_WEBSOCKET_NOTIFICATION'
const receivedWebsocketNotification = (notification) => ({
    type: RECEIVED_USER_WEBSOCKET_NOTIFICATION,
    notification
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
    fetchNotifications,
    removeNotification,
    receivedWebsocketNotification
}

export default function UserNotificationsReducer(state=INITIAL_STATE, action) {
    switch(action.type) {
        case NOTIFICATION_FETCH_SUCCESS:
            return {
                ...state, notifications: action.notifications
            }
        case REMOVE_NOTIFICATION:
            return {
                ...state, notifications: state.notifications.filter(x => x.id !== action.id)
            }
        case RECEIVED_USER_WEBSOCKET_NOTIFICATION:
            return {
                ...state, notifications: [...state.notifications, action.notification]
            }
        default:
            return state
    }
}
