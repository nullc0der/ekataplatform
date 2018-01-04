import {Component} from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'

import Helmet from 'react-helmet'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './App.styl'

import Header    from 'components/Header'
import LeftNav   from 'components/LeftNav'
import RightNav  from 'components/RightNav'
import SubHeader from 'components/SubHeader'
import Footer    from 'components/Footer'
import MiniChat  from 'components/HeaderMiniChat/MiniChat'
import OnlineUtil from 'components/OnlineUtil'

var debug = require('debug')('ekata:client:app')

class App extends Component {
	state = {
		isLeftNavOpen: false,
		isRightNavOpen: false
	}

	toggleLeftNav = ()=> {
		this.setState({isLeftNavOpen: !this.state.isLeftNavOpen})
	}
	toggleRightNav= ()=> {
		this.setState({isRightNavOpen: !this.state.isRightNavOpen})
	}

	render(){
		return (
			<section className={c.container}>
				<Helmet
					titleTemplate='%s | Ekata'
					defaultTitle='Ekata Social'/>
				<MiniChat/>
				<OnlineUtil/>
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

			</section>
		);
	}
}

const mapStateToProps = (state)=> ({
	showHeaders: state.Common.showHeaders
})

const mapDispatchToProps = (dispatch)=> ({

})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(App)
)
