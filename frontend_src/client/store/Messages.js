const debug = require('debug')('ekata:store:chat')

const INITIAL_STATE = {
    items: [],
    isLoading: false,
    hasErrored: false
}

const MESSAGE_IS_LOADING = 'MESSAGE_IS_LOADING'
const messagesIsLoading = (isLoading) => ({
    type: MESSAGE_IS_LOADING,
    isLoading
})

const M
