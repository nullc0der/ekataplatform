import {Component} from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './Home.styl'

class HomePage extends Component {
	render(){
		const cx = classnames(c.container)
		return (
			<section className={cx}>
				HomePage
			</section>
		)
	}
}

export default withStyles(c)(HomePage)
