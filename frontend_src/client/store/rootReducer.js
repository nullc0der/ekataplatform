import { combineReducers } from 'redux'
import { routerReducer as router } from 'react-router-redux'

import Chat from './Chat'
import Common from './Common'
import Groups from './Groups'
import Members from './Members'
import ChatRooms from './Chatrooms'
import Users from './Users'
import GroupSettings from './GroupSettings'
import GroupNotifications from './GroupNotifications'

export default combineReducers({
	router,
	Chat,
	Common,
	Groups,
	Members,
	ChatRooms,
	Users,
	GroupSettings,
	GroupNotifications
});
