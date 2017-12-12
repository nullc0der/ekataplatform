import { combineReducers } from 'redux'
import { routerReducer as router } from 'react-router-redux'

import Chat from './Chat'
import Common from './Common'
import Groups from './Groups'
import Members from './Members'

export default combineReducers({
	router,
	Chat,
	Common,
	Groups,
	Members
});