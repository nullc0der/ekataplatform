import {Component} from 'react'
import classnames from 'classnames'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './Avatar.styl'

class Avatar extends Component {

	render(){
		const {className, name = ''} = this.props;
		const initials = name.split(' ').slice(0, 2).map(x => x[0]).join('')
		const cx = classnames(c.container, 'ui-avatar', className)
		return (
			<div className={cx}>
				{ !!name && <div className='avatar-name'> {initials} </div> }
			</div>
		)
	}
}

export default withStyles(c)(Avatar)