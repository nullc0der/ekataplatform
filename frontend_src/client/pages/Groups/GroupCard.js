import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Groups.styl'

class GroupCard extends Component {
	render(){
		const {
			className,
			name,
			category,
			isSubscribed,
			imageURL,
			isAvailable,
			members,
			subscribers,
			active,
			shortDescription
		} = this.props;

		const cx = classnames(c.container, className, 'ui-group-card')

		return (
			<div className={cx}>
				<div className='card-inner'>
					<div className='card-header flex-horizontal j-between'>
						<div>
							<div className='name'> {name} </div>
							<div className='category'> {category} </div>
						</div>
						<div className='unsubscribe'> Unsubscribe </div>

						<div className={`card-circle-image ${isAvailable ? 'is-active' : ''}`}>
						</div>
					</div>

					<div className='card-body'>
						<h6> Short Description </h6>
						<p> {shortDescription} </p>

						<div className='bottom-stats flex-horizontal'>
							<div className='bottom-stat flex-1'>
								<div className='stat-value'> {members} </div>
								<div className='stat-label'> Members </div>
							</div>
							<div className='bottom-stat flex-1'>
								<div className='stat-value'> {subscribers} </div>
								<div className='stat-label'> Subscribers </div>
							</div>
							<div className='bottom-stat flex-1'>
								<div className='stat-value'> {active} </div>
								<div className='stat-label'> Active </div>
							</div>
						</div>

					</div>
				</div>
				<div className='card-action'>
					Invite Others
				</div>
			</div>
		)
	}
}

export default GroupCard
