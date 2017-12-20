import request from 'superagent'
import _ from 'lodash'
const debug = require('debug')('ekata:store:chat')

import CHAT_LIST from 'pages/Messenger/sample-chats'
import CHAT_DETAILS from 'pages/Messenger/sample-detailed-chat'

const INITIAL_STATE = {
	minichats: [],
	chats: [],
	areLoading: false,
    hasErrored: false
}

function createSampleChat(chat){
	return Object.assign({}, chat, {user: chat.username, messages: CHAT_DETAILS})
}

const OPEN_MINI_CHAT = 'OPEN_MINI_CHAT'
const openMiniChat = (chat)=> ({
	type: OPEN_MINI_CHAT,
	chat: createSampleChat(chat)
})


const CLOSE_MINI_CHAT = 'CLOSE_MINI_CHAT'
const closeMiniChat = (chatid)=> ({
	type: CLOSE_MINI_CHAT,
	chatid
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
const chatsFetchDataSuccess = (chats) => ({
    type: CHATS_FETCH_DATA_SUCCESS,
    chats
})

const CHAT_SEND_SUCCESS = 'CHAT_SEND_SUCCESS'
const chatSendSuccess = (chat) => ({
    type: CHAT_SEND_SUCCESS,
    chat
})

const RECEIVED_CHAT_ON_WEBSOCKET = 'RECEIVED_CHAT_ON_WEBSOCKET'
export const receivedChatOnWebsocket = (chat) => ({
    type: RECEIVED_CHAT_ON_WEBSOCKET,
    chat
})

const CLEAR_CHAT = 'CLEAR_CHAT'
export const clearChat = (roomId) => ({
    type: CLEAR_CHAT,
    roomId
})

const DELETE_CHATS = 'DELETE_CHATS'
export const deleteChats = (chatIds) => ({
    type: DELETE_CHATS,
    chatIds
})

export const chatsFetchData = (url) => { 
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
                    dispatch(chatsFetchDataSuccess(res.body))
                    dispatch(chatsAreLoading(false))
                }
            })
    }
}

export const sendChat = (url, content) => {
    return (dispatch) => {
        request
            .post(url)
            .set('X-CSRFToken', window.django.csrf)
            .send({'content': content})
            .end((err, res) => {
                if (res.ok) {
                    dispatch(chatSendSuccess(res.body))
                }
            })
    }
}

export const sendDeleteChat = (url, ids) => {
    return (dispatch) => {
        request
            .post(url)
            .set('X-CSRFToken', window.django.csrf)
            .type('form')
            .send({ 'ids': ids })
            .end((err, res) => {
                if (res.ok) {
                    if (res.body.length) {
                        dispatch(deleteChats(res.body))
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
			return {...state, minichats: [...state.minichats, action.chat]}
		case CLOSE_MINI_CHAT:
			return {...state, minichats: state.minichats.filter(x => x.id !== action.chatid )}
		case CHATS_ARE_LOADING:
            return {...state, areLoading: action.areLoading}
        case CHATS_HAS_ERRORED:
            return {...state, hasErrored: action.hasErrored}
        case CHATS_FETCH_DATA_SUCCESS:
            return {...state, chats: action.chats}
        case CHAT_SEND_SUCCESS:
            return {...state, chats: [...state.chats, action.chat]}
        case RECEIVED_CHAT_ON_WEBSOCKET:
            return {...state, chats: [...state.chats, action.chat]}
        case CLEAR_CHAT:
            return {...state, chats: []}
        case DELETE_CHATS:
            return {...state, chats: state.chats.filter(chat => !(_.includes(action.chatIds, chat.id)))}
		default:
			return state
	}
}
