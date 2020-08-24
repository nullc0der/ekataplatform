import request from 'superagent'


const INITIAL_STATE = {
    notifications: []
}

const NOTIFICATIONS_LOAD_SUCCESS = 'NOTIFICATIONS_LOAD_SUCCESS'
const notificationsLoadSuccess = (notifications) => ({
    type: NOTIFICATIONS_LOAD_SUCCESS,
    notifications
})

const NOTIFICATION_CREATE_SUCCESS = 'NOTIFICATION_CREATE_SUCCESS'
const notificationCreateSuccess = (notification) => ({
    type: NOTIFICATION_CREATE_SUCCESS,
    notification
})

const NOTIFICATION_DELETE_SUCCESS = 'NOTIFICATION_DELETE_SUCCESS'
const notificationDeleteSuccess = (notificationID) => ({
    type: NOTIFICATION_DELETE_SUCCESS,
    notificationID
})

const NOTIFICATION_EDIT_SUCCESS = 'NOTIFICATION_EDIT_SUCCESS'
const notificationEditSuccess = (notification) => ({
    type: NOTIFICATION_EDIT_SUCCESS,
    notification
})

const loadNotifications = (url) => {
    return (dispatch) => {
        request
            .get(url)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(notificationsLoadSuccess(res.body))
                }
            })
    }
}

const createNotification = (url, payload) => {
    return (dispatch) => {
        request
            .post(url)
            .set('X-CSRFToken', window.django.csrf)
            .send(payload)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(notificationCreateSuccess(res.body))
                }
            })
    }
}

const deleteNotification = (url, id) => {
    return (dispatch) => {
        request
            .delete(url)
            .set('X-CSRFToken', window.django.csrf)
            .send({'id': id})
            .end((err, res) => {
                if (res.status === 204) {
                    dispatch(notificationDeleteSuccess(id))
                }
            })
    }
}

const updateNotification = (url, payload) => {
    return (dispatch) => {
        request
            .put(url)
            .set('X-CSRFToken', window.django.csrf)
            .send(payload)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(notificationEditSuccess(res.body))
                }
            })
    }
}

export const actions = {
    loadNotifications,
    createNotification,
    deleteNotification,
    updateNotification
}

export default function GroupNotificationReducer(state=INITIAL_STATE, action) {
    switch(action.type) {
        case NOTIFICATIONS_LOAD_SUCCESS:
            return {
                ...state, notifications: action.notifications
            }
        case NOTIFICATION_CREATE_SUCCESS:
            return {
                ...state, notifications: [
                    ...state.notifications, action.notification
                ]
            }
        case NOTIFICATION_DELETE_SUCCESS:
            return {
                ...state, notifications: state.notifications.filter(x => x.id !== action.notificationID)
            }
        case NOTIFICATION_EDIT_SUCCESS:
            return {
                ...state, notifications: state.notifications.map(x => {
                    return x.id === action.notification.id ? action.notification : x
                })
            }
        default:
            return state
    }
}
