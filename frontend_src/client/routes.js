import Route         from 'react-router/lib/Route'
import Redirect      from 'react-router/lib/Redirect'
import IndexRedirect from 'react-router/lib/IndexRedirect'
import IndexRoute    from 'react-router/lib/IndexRoute'

// In production mode,
// client bundler will replace 'SyncRouteConfig' with 'AsyncRouteConfig'
import getRouteConfig from './SyncRouteConfig'
import getRouteUtils  from './RouteUtils'

import App from './containers/App'

export default function getRoutes(store, req, res){
	const Utils = getRouteUtils(store, req, res)
	const Pages = getRouteConfig(store, req, res)

	return (
		<Route path='/' component={App}>
			<IndexRoute getComponent={Pages.Home}/>
			<Route path='messenger/(:id)' getComponent={Pages.Messenger}/>
			<Route path='community'>
				<IndexRedirect to='groups'/>
				<Route path='groups' getComponent={Pages.Groups}/>
			</Route>
			<Route path='groups'>
				<IndexRedirect to='members'/>
				<Route path='members' getComponent={Pages.Groups_Members}/>
			</Route>
			<Redirect from='*' to='/'/>
		</Route>
	)
}
