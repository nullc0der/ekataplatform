import Home from './pages/Home'
import Messenger from './pages/Messenger'
import Groups    from './pages/Groups'
import Groups_Members from './pages/Groups/Members'
import PublicMembers from './pages/PublicMembers'
import ErrorPage from './pages/ErrorPage'
import Groups_Settings from './pages/Groups/Settings'

export default function getSyncRouteConfig(store, req, res){
	return {
		Home: (nextState, cb)=> {
			cb(null, Home)
		},
		Messenger: (nextState, cb)=> {
			cb(null, Messenger)
		},
		Groups: (nextState, cb)=> {
			cb(null, Groups)
		},
		Groups_Members: (nextState, cb)=> {
			cb(null, Groups_Members)
		},
		PublicMembers: (nextState, cb)=> {
			cb(null, PublicMembers)
		},
		ErrorPage: (nextState, cb)=> {
			cb(null, ErrorPage)
		},
		Groups_Settings: (nextState, cb) => {
			cb(null, Groups_Settings)
		}
	}
}
