import request from 'superagent'
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

export const chatsFetchData = (url) => { 
    return (dispatch) => {
        dispatch(chatsAreLoading(true))
        request
            .get(url)
            .set('Accept', 'application/json')
            .end((err, res) => {
                if (err || !res.ok) {
                    dispatch(chatsHasErrored(true))
                } else {
                    dispatch(chatsFetchDataSuccess(res.body))
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
		default:
			return state
	}
}
