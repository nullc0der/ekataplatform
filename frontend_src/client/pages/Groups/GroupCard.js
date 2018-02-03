import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Groups.styl'

class GroupCard extends Component {
	render(){
		const {
			className,
			id,
			groupURL,
			name,
			category,
			isSubscribed,
			isMember,
			joinRequestSent,
			//headerURL,
			logoURL,
			members,
			subscribers,
			shortDescription,
			onSubscribeButtonClick,
			onJoinButtonClick
		} = this.props;

		const cx = classnames(c.container, className, 'ui-group-card', 'group-type-' + category.toLowerCase())

		return (
			<a href={groupURL} style={{textDecoration: "none"}}>
				<div className={cx}>
					<div className='card-inner'>
						<div className='card-header flex-horizontal j-between'>
							<div>
								<div className='name'> {name} </div>
								<div className='category'> {category.split(" ").join("\n")} </div>
							</div>
							<div className='unsubscribe'
								 onClick={(e) => onSubscribeButtonClick(e, id, !isSubscribed?true:false)}>
									{isSubscribed ? 'Unsubscribe' : 'Subscribe'} </div>

							<div className='card-circle-image' style={{backgroundImage: `url(${logoURL})`}}>
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
								{/* <div className='bottom-stat flex-1'>
									<div className='stat-value'> {active} </div>
									<div className='stat-label'> Active </div>
								</div> */}
							</div>

						</div>
					</div>
					<div className='card-action' onClick={(e) => onJoinButtonClick(e, id, isMember ? "leave" : joinRequestSent ? "cancel" : "join")}>
						{isMember ? "Leave group" : joinRequestSent ? "Cancel Request" : "Join group"}
					</div>
				</div>
			</a>
		)
	}
}

export default GroupCard
