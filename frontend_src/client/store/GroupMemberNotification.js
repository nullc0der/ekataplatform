import request from 'superagent'

const INITIAL_STATE = {
    notifications: [],
    isLoading: false
}

const MEMBER_NOTIFICATION_LOAD_SUCCESS = 'MEMBER_NOTIFICATION_LOAD_SUCCESS'
const memberNotificationLoadSuccess = (notifications) => ({
    type: MEMBER_NOTIFICATION_LOAD_SUCCESS,
    notifications
})

const REMOVE_MEMBER_NOTIFICATION = 'REMOVE_MEMBER_NOTIFICATION'
const removeMemberNotification = (notificationID) => ({
    type: REMOVE_MEMBER_NOTIFICATION,
    notificationID
})

const RECEIVED_WEBSOCKET_NOTIFICATION = 'RECEIVED_WEBSOCKET_NOTIFICATION'
const receivedWebsocketNotification = (notification) => ({
    type: RECEIVED_WEBSOCKET_NOTIFICATION,
    notification
})

const CHANGE_LOADING_STATUS = 'CHANGE_LOADING_STATUS'
const changeLoadingStatus = (status) => ({
  type: CHANGE_LOADING_STATUS,
  status
})

const loadMemberNotifications = (url) => {
    return (dispatch) => {
        dispatch(changeLoadingStatus(true))
        request
            .get(url)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(memberNotificationLoadSuccess(res.body))
                    dispatch(changeLoadingStatus(false))
                }
            })
    }
}

const setNotificationRead = (url, notificationID) => {
    return (dispatch) => {
        request
            .put(url)
            .set('X-CSRFToken', window.django.csrf)
            .send({'id': notificationID})
            .end((err, res) => {
                if (res.ok) {
                    dispatch(removeMemberNotification(notificationID))
                }
            })
    }
}

export const actions = {
    loadMemberNotifications,
    removeMemberNotification,
    setNotificationRead,
    receivedWebsocketNotification
}

export default function GroupMemberNotificationReducer(state=INITIAL_STATE, action) {
    switch (action.type) {
        case MEMBER_NOTIFICATION_LOAD_SUCCESS:
            return {
                ...state, notifications: action.notifications
            }
        case REMOVE_MEMBER_NOTIFICATION:
            return {
                ...state, notifications: state.notifications.filter(x => x.notification_id !== action.notificationID)
            }
        case RECEIVED_WEBSOCKET_NOTIFICATION:
            return {
                ...state, notifications: [...state.notifications, action.notification]
            }
        case CHANGE_LOADING_STATUS:
            return {
                ...state, isLoading: action.status
            }
        default:
            return state
    }
}
