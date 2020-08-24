import {Component} from 'react'
import classnames  from 'classnames'
import request from 'superagent'
import {isEmpty} from 'lodash'

class GroupCard extends Component {

	state = {
		group: {}
	}

	// TODO: Get this from parent
	componentDidMount() {
		const id = this.props.groupID
		request
			.get(`/api/groups/${id}/details/`)
			.end((err, res) => {
				if (res.ok) {
					this.setState({
						group: res.body
					})
				}
			})
	}

	render(){
		const {
			className
		} = this.props

		const {
			group
		} = this.state

		const cardActionTexts = {
			"open": "Join Group",
			"closed": "Closed Group",
			"request": "Request to Join",
			"invite": "Invitation Only"
		}

		const cx = classnames(className, 'ui-group-card', 'group-type-' + (group.group_type ? group.group_type.toLowerCase(): 'other'))

		return (
			<div className={cx}>
				{!isEmpty(group) && <div className='card-inner'>
					<div className='card-header flex-horizontal'>
						<div className="group-header-image" style={{ backgroundImage: `url(${group.header_image_url || ''})` }}>

						</div>
						<div className="group-info">
							<div className='name'> {group.name} </div>
							<div className='category'> {group.group_type.split(" ").join("\n")} </div>
						</div>
					</div>
					<div className='card-circle-image' style={{ backgroundImage: `url(${group.logo_url})` }}>
					</div>

					<div className='card-body'>
						<h6> Short Description </h6>
						<p> {group.description} </p>
					</div>
				</div>}
			</div>
		)
	}
}

export default GroupCard
