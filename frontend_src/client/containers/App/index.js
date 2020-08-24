import {Component} from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'
import Websocket from 'react-websocket'

import Helmet from 'react-helmet'
import NotificationSystem from 'react-notification-system'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './App.styl'

import Header    from 'components/Header'
import LeftNav   from 'components/LeftNav'
import RightNav  from 'components/RightNav'
import SubHeader from 'components/SubHeader'
import Footer    from 'components/Footer'
import MiniChat  from 'components/HeaderMiniChat/MiniChat'
import OnlineUtil from 'components/OnlineUtil'
import {actions as userNotificationActions} from 'store/UserNotifications'

var debug = require('debug')('ekata:client:app')

class App extends Component {
	state = {
		isLeftNavOpen: false,
		isRightNavOpen: false
	}

	_notificationSystem = null

	style = {
		NotificationItem: { 
			DefaultStyle: { 
				margin: '20px 5px 2px 1px'
			}
		}
	}

	componentDidMount = () => {
		this._notificationSystem = this.refs.notificationSystem
	}

	componentDidUpdate = (prevProps) => {
		if (prevProps.notification !== this.props.notification) {
			this._notificationSystem.addNotification(this.props.notification)
		}
	}

	toggleLeftNav = ()=> {
		this.setState({isLeftNavOpen: !this.state.isLeftNavOpen})
	}
	toggleRightNav= ()=> {
		this.setState({isRightNavOpen: !this.state.isRightNavOpen})
	}

	onWebsocketMessage = (data) => {
		const result = JSON.parse(data)
		if (result.notification) {
			this.props.receivedWebsocketNotification(result.notification)
		}
	}

	render(){
		const websocket_url = `${window.location.protocol == "https:" ? "wss" : "ws"}` + '://' + window.location.host + "/notifications/stream/"
		return (
			<section className={c.container}>
				<Helmet
					titleTemplate='%s | Ekata'
					defaultTitle='Ekata Social'/>
				<MiniChat/>
				<OnlineUtil/>
				<NotificationSystem ref="notificationSystem" style={this.style} />
				<LeftNav
					className={c.leftNav}
					open={this.state.isLeftNavOpen}
					onRequestToggle={this.toggleLeftNav}/>

				<section className={c.content}>
					<Header
						className={c.header}
						onMenuToggle={this.toggleLeftNav}
						onSettingsToggle={this.toggleRightNav}
						showHeaders={this.props.showHeaders ? true: false }/>
					<SubHeader
						className={c.subHeader}
						showHeaders={this.props.showHeaders ? true : false}/>
					<section className='content-inner flex-vertical'>
						{this.props.children}
					</section>
					<Footer/>
				</section>

				<RightNav
					className={c.rightNav}
					open={this.state.isRightNavOpen}
					onRequestClose={this.toggleLeftNav}/>
				<Websocket url={websocket_url}
					onMessage={this.onWebsocketMessage.bind(this)} />
			</section>
		);
	}
}

const mapStateToProps = (state)=> ({
	showHeaders: state.Common.showHeaders,
	notification: state.Common.notification
})

const mapDispatchToProps = (dispatch)=> ({
	receivedWebsocketNotification: (notification) => {
		dispatch(userNotificationActions.receivedWebsocketNotification(notification))
	}
})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(App)
)
