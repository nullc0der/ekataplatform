import React    from 'react'
import {render} from 'react-dom'

import createHistory  from 'history/lib/createBrowserHistory'

import Router from 'react-router/lib/Router'
import match  from 'react-router/lib/match'
import useRouterHistory from 'react-router/lib/useRouterHistory'
// import injectTapEventPlugin from 'react-tap-event-plugin';

import { syncHistoryWithStore } from 'react-router-redux'

import configureStore, { loadState, saveState, storageSupported } from './store'
import getRoutes from './routes'
import WithStylesContext from 'utils/withStylesContext'
import throttle from 'lodash/throttle'
import merge from 'lodash/merge'
import $ from 'jquery'

import Root from './containers/Root'
import * as OfflinePluginRuntime from 'offline-plugin/runtime';

var debug = require('debug')('ekata:client')

window.$ = window.jQuery = $;
// injectTapEventPlugin();


var browserHistory = useRouterHistory(createHistory)({
	queryKey: false,
	basename: '/'
});

var initialState = window.INITIAL_STATE || {};
var savedState = {}; //loadState()
// Priority to server sent state
var finalState = merge({}, initialState, savedState);
var store   = configureStore(finalState, browserHistory);
var history = syncHistoryWithStore(browserHistory, store, {
  selectLocationState: (state) => state.router
});

window.localStorage.debug = 'ekata:*';

const ROOT_CONTAINER = document.getElementById('root');
const SERVER_CSS = document.getElementById('server-css');
const onRenderComplete = ()=> {
	console.timeEnd('render');
	document.head.removeChild(SERVER_CSS)
}

if ( __DEV__ ){
	window.React = React;
	window._History = history;
	window._STORE = store;
}


// const render = (routes, Root)=> {
// 	console.time('render');
// 		ReactDOM.render(
// 			<Root store={store}>
// 				<Router history={history}>
// 					{routes}
// 				</Router>
// 			</Root>
// 			, ROOT_CONTAINER
// 			, onRenderComplete
// 		)
// }

const renderApp = (routes, Root)=> {
	console.time('render');
		render(
			<Root store={store}>
				<WithStylesContext onInsertCss={styles=> styles._insertCss()}>
					<Router history={history}>
						{routes}
					</Router>
				</WithStylesContext>
			</Root>
			, ROOT_CONTAINER
			, onRenderComplete
		)
}


renderApp(getRoutes(store), Root)


if (process.env.NODE_ENV === "production"){
	OfflinePluginRuntime.install({
		onUpdateReady: ()=> {
			console.info('SW Event: Update Ready. Applying...')
		},
		onUpdated: ()=> {
			console.info('SW Event: Applied.')
			// window.location.reload();
		}
	});
}

NProgress.set(0.6)

$(document).ready(function(){
	// On document ready finish nprogress
	NProgress.done()
	var requestCounter = 0;

	$(document).on('ajaxSend', function(){
		NProgress.start()
		console.log('reqCounter: ', ++requestCounter)
	})

	$(document).on('ajaxComplete', function(){
		NProgress.done()
		console.log('reqCounter: ', --requestCounter)
	})

	window.scrollTo(0, -1)
})
