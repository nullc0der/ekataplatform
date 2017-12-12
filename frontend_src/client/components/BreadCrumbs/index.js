import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './BreadCrumbs.styl'

import withRouter from 'react-router/lib/withRouter'

const debug = require('debug')('ekata:comp:breadcrumbs')

class BreadCrumbs extends Component {
	static ui = c

	render(){
		const {
			className,
			title,
			list,
			current,
			location
		} = this.props;

		const cx = classnames(c.container, className)
		// debug('Setting Props: ', this.props)

		return (
			<div className={cx}>
				BreadCrumbs
			</div>
		)
	}
}

export default withStyles(c)(
	withRouter(BreadCrumbs)
)
