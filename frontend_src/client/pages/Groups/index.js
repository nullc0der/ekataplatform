import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Groups.styl'

import {connect} from 'react-redux'
import GroupCard from './GroupCard'

class GroupsPage extends Component {
	render(){
		const {
			className,
			list
		} = this.props;

		const cx = classnames(c.container, className)

		return (
			<div className={cx}>
				{
					list.map((x,i)=> {

						return <GroupCard
							key={i}
							id={x.id}
							name={x.name}
							isAvailable={x.is_available}
							category={x.category}
							imageURL={x.image_url}
							isSubscribed={x.is_subscribed}
							shortDescription={x.short_description}
							members={x.stats.members}
							subscribers={x.stats.subscribers}
							active={x.stats.active}
							/>
					})
				}
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	list: state.Groups.groups
})

const mapDispatchToProps = (dispatch)=> ({

})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(GroupsPage)
)
