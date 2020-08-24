import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import find from 'lodash/find'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import Avatar  from 'components/Avatar'

class MemberItem extends Component {

	renderSubscribedGroup = (group_id, i) => {
		const { groups = [] } = this.props;
		const g = find(groups, { id: group_id }) || {}

		const name = g.name || ''
		const icon = g.icon || {}

		return <div key={i} className={`group-item flex-horizontal a-center j-center group-id-${g.id}`} title={name}>
			{icon.type === 'material' ? <i className='material-icons'> {icon.name} </i> : <i className={`fa fa-${icon.name}`}></i> }
		</div>
	}

	render(){
		const {
			className,
			isOnline,
			userName = '',
			fullName = '',
			avatarUrl = '',
			avatarColor = '',
			publicURL = '',
			subscribed_groups = [],
			groups = []
		} = this.props;

		const cx = classnames(className, 'ui-member-item', 'flex-horizontal j-between')

		return (
			<div className={cx}>
				<div className='flex-horizontal a-center flex-1'>
					<div className='in-left flex-horizontal a-center'>
						<a href={publicURL}>
							{
								avatarUrl ?
									<img className='avatar-image rounded' src={avatarUrl} /> :
									<Avatar className='avatar-image' name={fullName || userName} bgcolor={avatarColor} />
							}
						</a>
						<div className='details'>
							<div className='name'> {fullName || userName} <span className='username'>@{userName}</span> </div>
							<div className={`status is-${isOnline? "online": "offline"}`}> {isOnline? "Online" : "Offline"} </div>
						</div>
					</div>
					<div className='in-right flex-horizontal flex-1'>
						<div
							className='subscribed-groups flex-horizontal-reverse a-center'>
							{
								!subscribed_groups.length
									? 	<div className='group-item flex-horizontal a-center j-center'>
											<i className='material-icons'>add_circle</i>
										</div>
									: subscribed_groups.map(this.renderSubscribedGroup)
							}
						</div>
					</div>
				</div>
			</div>
		)
	}
}

export default MemberItem
