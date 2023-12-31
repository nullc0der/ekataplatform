export default function getAsyncRouteConfig(store, req, res){
	return {
		Home: (nextState, cb)=> {
			require.ensure([], (require)=> {
				var comp = require('./pages/Home')
				cb(null, comp.default)
			}, 'HomePage')
		},
		Messenger: (nextState, cb)=> {
			require.ensure([], (require)=> {
				var comp = require('./pages/Messenger')
				cb(null, comp.default)
			}, 'MessengerPage')
		},
		Groups: (nextState, cb)=> {
			require.ensure([], (require)=> {
				var comp = require('./pages/Groups')
				cb(null, comp.default)
			}, 'GroupsPage')
		},
		Groups_Members_Management: (nextState, cb)=> {
			require.ensure([], (require)=> {
				var comp = require('./pages/Groups/MembersManagement')
				cb(null, comp.default)
			}, 'Groups-Members-Management')
		},
		Groups_Members: (nextState, cb) => {
			require.ensure([], (require) => {
				var comp = require('./pages/Groups/Members')
				cb(null, comp.default)
			}, 'Groups-Members')
		},
		PublicMembers: (nextState, cb) => {
			require.ensure([], (require) => {
				var comp = require('./pages/PublicMembers')
				cb(null, comp.default)
			}, 'PublicMembers')
		},
		ErrorPage: (nextState, cb) => {
			require.ensure([], (require) => {
				var comp = require('./pages/ErrorPage')
				cb(null, comp.default)
			}, 'ErrorPage')
		},
		Groups_Settings: (nextState, cb) => {
			require.ensure([], (require) => {
				var comp = require('./pages/Groups/Settings')
				cb(null, comp.default)
			}, 'Groups-Settings')
		},
		Group_Posts: (nextState, cb) => {
			require.ensure([], (require) => {
				var comp = require('./pages/Groups/PostPage')
				cb(null, comp.default)
			}, 'Group-Posts')
		}
	}
}
