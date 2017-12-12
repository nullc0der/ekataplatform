import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './SubHeader.styl'

import {connect} from 'react-redux'
import Link from 'react-router/lib/Link'

import startCase from 'lodash/startCase'
import take from 'lodash/take'

class SubHeader extends Component {
	render(){
		const {
			className,
			location
		} = this.props;

		const cx = classnames(c.container, className, 'flex-horizontal', 'a-center')

		const paths = location.pathname.split('/').filter(x => !!x)
		const mainPath = startCase(paths[paths.length-1])

		const crumbs = paths.map((x,i) => {
			return {
				href: location.basename + take(paths, i+1).join('/'),
				text: startCase(x)
			}
		})

		// console.log(paths)

		return (
			<div className={cx}>
				<div>
					<div className='title'> {mainPath} </div>
					<div className='list-links flex-horizontal'>
						{
							crumbs.map((x,i)=> {
								return <Link
									to={x.href}
									className='bread-link'
									key={i}> {x.text} / </Link>
							})
						}
					</div>
				</div>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	location: state.router.locationBeforeTransitions
})

const mapDispatchToProps = (dispatch)=> ({

})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(SubHeader)
)
