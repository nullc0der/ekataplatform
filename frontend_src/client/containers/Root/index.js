import { Component } from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'

class Root extends Component {
	static propTypes = {
		store: PropTypes.object.isRequired,
	};

	render () {
		return (
			<Provider store={this.props.store}>
				<div className='root-inner'>
					{this.props.children}
				</div>
			</Provider>
		)
	}
}

export default Root