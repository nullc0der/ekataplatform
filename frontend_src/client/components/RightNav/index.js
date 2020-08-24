import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './RightNav.styl'

import Tabs from 'react-bootstrap/lib/Tabs'
import Tab  from 'react-bootstrap/lib/Tab'

class RightNav extends Component {
	state = {
		selected: 0
	}

	switchTab = (selected)=> {
		this.setState({selected})
	}

	render(){
		const {
			className,
			open
		} = this.props;

		const cx = classnames(c.container, className, {
			'is-open': open
		})

		return (
			<div className={cx}>
				<Tabs
					id='rightnav-tabs'
					className='rightnav-tabs'
					activeKey={this.state.selected}
					onSelect={this.switchTab}>
					<Tab
						className='rightnav-tab'
						eventKey={0}
						title={<i className='fa fa-fw fa-wrench'/>}>
						Content 1

					</Tab>
					<Tab
						className='rightnav-tab'
						eventKey={1}
						title={<i className='fa fa-fw fa-home'/>}>
						Content 2
					</Tab>
					<Tab
						className='rightnav-tab'
						eventKey={2}
						title={<i className='fa fa-fw fa-cogs'/>}>
						Content 3
					</Tab>
				</Tabs>
			</div>
		)
	}
}

export default withStyles(c)(RightNav)
