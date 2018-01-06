import request from 'superagent'
import _ from 'lodash'
const debug = require('debug')('ekata:store:chat')

const INITIAL_STATE = {
	minichats: [],
	chats: {},
	areLoading: false,
    hasErrored: false,
    uploadProgress: {}
}

const OPEN_MINI_CHAT = 'OPEN_MINI_CHAT'
const openMiniChat = (roomId)=> ({
	type: OPEN_MINI_CHAT,
	roomId
})


const CLOSE_MINI_CHAT = 'CLOSE_MINI_CHAT'
const closeMiniChat = (roomId)=> ({
	type: CLOSE_MINI_CHAT,
	roomId
})

const CHATS_ARE_LOADING = 'CHATS_ARE_LOADING'
const chatsAreLoading = (areLoading) => ({
    type: CHATS_ARE_LOADING,
    areLoading
})

const CHATS_HAS_ERRORED = 'CHATS_HAS_ERRORED'
const chatsHasErrored = (hasErrored) => ({
    type: CHATS_HAS_ERRORED,
    hasErrored
})

const CHATS_FETCH_DATA_SUCCESS = 'CHATS_FETCH_DATA_SUCCESS'
const chatsFetchDataSuccess = (roomId, chats) => ({
    type: CHATS_FETCH_DATA_SUCCESS,
    roomId,
    chats
})

const CHAT_SEND_SUCCESS = 'CHAT_SEND_SUCCESS'
const chatSendSuccess = (roomId, chat) => ({
    type: CHAT_SEND_SUCCESS,
    roomId,
    chat
})

const RECEIVED_CHAT_ON_WEBSOCKET = 'RECEIVED_CHAT_ON_WEBSOCKET'
export const receivedChatOnWebsocket = (roomId, chat) => ({
    type: RECEIVED_CHAT_ON_WEBSOCKET,
    roomId,
    chat
})

const CLEAR_CHAT = 'CLEAR_CHAT'
export const clearChat = (roomId) => ({
    type: CLEAR_CHAT,
    roomId
})

const DELETE_CHATS = 'DELETE_CHATS'
export const deleteChats = (roomId, chatIds) => ({
    type: DELETE_CHATS,
    roomId,
    chatIds
})

const UPDATE_CHAT_READ_STATUS = 'UPDATE_CHAT_READ_STATUS'
export const updateChatReadStatus = (roomId, chatIds) => ({
    type: UPDATE_CHAT_READ_STATUS,
    roomId,
    chatIds
})

const FILE_UPLOAD_PROGRESS = 'FILE_UPLOAD_PROGRESS'
const fileUploadProgress = (roomId, progress) => ({
    type: FILE_UPLOAD_PROGRESS,
    roomId,
    progress
})

export const chatsFetchData = (url, roomId) => { 
    return (dispatch) => {
        dispatch(chatsAreLoading(true))
        request
            .get(url)
            .set('Accept', 'application/json')
            .end((err, res) => {
                if (err || !res.ok) {
                    dispatch(chatsHasErrored(true))
                    dispatch(chatsAreLoading(false))
                } else {
                    dispatch(chatsFetchDataSuccess(roomId, res.body))
                    dispatch(chatsAreLoading(false))
                }
            })
    }
}

export const sendChat = (url, roomId, content, file=null) => {
    return (dispatch) => {
        if (file) {
            request
                .post(url)
                .set('X-CSRFToken', window.django.csrf)
                .attach('file', file)
                .field({ 'content': content })
                .on('progress', event => {
                    dispatch(fileUploadProgress(roomId, event.percent))
                })
                .end((err, res) => {
                    if (res.ok) {
                        dispatch(chatSendSuccess(roomId, res.body))
                    }
                    dispatch(fileUploadProgress(roomId, 0))
                })
        }
        else {
            request
                .post(url)
                .set('X-CSRFToken', window.django.csrf)
                .send({ 'content': content })
                .end((err, res) => {
                    if (res.ok) {
                        dispatch(chatSendSuccess(roomId, res.body))
                    }
                })
        }
    }
}

export const sendDeleteChat = (url, roomId, ids) => {
    return (dispatch) => {
        request
            .post(url)
            .set('X-CSRFToken', window.django.csrf)
            .type('form')
            .send({ 'ids': ids })
            .end((err, res) => {
                if (res.ok) {
                    if (res.body.length) {
                        dispatch(deleteChats(roomId, res.body))
                    }
                }
            })
    }
}

export const actions = {
	openMiniChat,
	closeMiniChat
}

export default function ChatReducer(state = INITIAL_STATE, action){
	switch(action.type){
        case OPEN_MINI_CHAT:
            let roomIdExist = state.minichats.indexOf(action.roomId) > -1
            let minichats = state.minichats.slice()
            if (!roomIdExist) {
                minichats.push(action.roomId)
            }
			return {...state, minichats: minichats}
		case CLOSE_MINI_CHAT:
			return {...state, minichats: state.minichats.filter(x => x !== action.roomId)}
		case CHATS_ARE_LOADING:
            return {...state, areLoading: action.areLoading}
        case CHATS_HAS_ERRORED:
            return {...state, hasErrored: action.hasErrored}
        case CHATS_FETCH_DATA_SUCCESS:
            return {...state, chats: {...state.chats, [action.roomId]: action.chats}}
        case CHAT_SEND_SUCCESS:
            return {
                ...state,
                chats: {
                    ...state.chats,
                    [action.roomId]: [...state.chats[action.roomId], action.chat]
                }
            }
        case RECEIVED_CHAT_ON_WEBSOCKET:
            return {
                ...state,
                chats: {
                    ...state.chats,
                    [action.roomId]: [...state.chats[action.roomId], action.chat]
                }
            }
        case CLEAR_CHAT:
            return {...state, chats: {
                ...state.chats,
                [action.roomId]: []
            }}
        case DELETE_CHATS:
            return {...state, chats: {
                ...state.chats,
                [action.roomId]: state.chats[action.roomId].filter(chat => !(_.includes(action.chatIds, chat.id)))}}
        case FILE_UPLOAD_PROGRESS:
            return {...state, uploadProgress: {roomId: action.roomId, progress: action.progress}}
        case UPDATE_CHAT_READ_STATUS:
            return {...state, chats: {
                ...state.chats,
                [action.roomId]: state.chats[action.roomId].map(chat => {
                    return _.includes(action.chatIds, chat.id)? {...chat, read:true}: chat
                })
            }}
		default:
			return state
	}
}
