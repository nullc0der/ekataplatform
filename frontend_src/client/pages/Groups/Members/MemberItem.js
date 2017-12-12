import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import find from 'lodash/find'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import Avatar  from 'components/Avatar'
import chunk from 'lodash/chunk'
import Modal from 'components/ui/Modal'

class MemberItem extends Component {

	state = {
		subscribeBoxIsOpen: false
	}

	toggleGroup = (group)=> {
		this.props.toggleSubscribedGroup(
			this.props.memberId,
			group
		)
	}

	renderGroup = (group, i)=> {
		const {subscribed_groups = []} = this.props;
		const cx = classnames('subscribe-box-group group-item', {
			'is-inactive': subscribed_groups.indexOf(group.id) === -1
		})
		return <div
			key={i}
			onClick={(e)=> this.toggleGroup(group)}
			className={cx}>
			<div className='group-icon'>
				<i className='material-icons'> {group.icon} </i>
			</div>
			<div className='group-name'> {group.name} </div>
		</div>
	}

	renderSubscribedGroup = (group_id, i)=> {
		const {groups = []} = this.props;
		const g = find(groups, {id: group_id}) || {}

		const name = g.name || 'Group Name'
		const icon = g.icon || 'Group Icon'

		return <div key={i} className='group-item flex-horizontal a-center j-center' title={name}>
			<i className='material-icons'> {icon} </i>
		</div>
	}

	toggleSubscribeBox = ()=> {
		this.setState({
			subscribeBoxIsOpen: !this.state.subscribeBoxIsOpen
		})
	}

	render(){
		const {
			className,
			name = '',
			status = '',
			subscribed_groups = [],
			groups = []
		} = this.props;

		const cx = classnames(className, 'ui-member-item', 'flex-horizontal j-between')

		const gchunks = chunk(groups, 4)

		return (
			<div className={cx}>
				<Modal
					id='edit-group-subscriptions'
					onBackdropClick={this.toggleSubscribeBox}
					isOpen={this.state.subscribeBoxIsOpen}
					title={false}>
					<div className='subscribe-box'>
						{
							gchunks.map((x,i)=> (
								<div key={i} className={`box flex-horizontal a-center box-${i+1}`}>
									{
										x.map((y, j)=> this.renderGroup(y, i.toString() + j.toString()))
									}
								</div>
							))
						}
					</div>
				</Modal>
				<div
					onClick={this.toggleSubscribeBox}
					className='flex-horizontal a-center flex-1'>
					<div className='in-left flex-horizontal a-center'>
						<Avatar
							name={name}/>
						<div className='details'>
							<div className='name'> {name} </div>
							<div className={`status is-${status.toLowerCase()}`}> {status} </div>
						</div>
					</div>
					<div className='in-right flex-horizontal flex-1'>
						<div
							className='subscribed-groups flex-horizontal-reverse a-center'>
							{
								!subscribed_groups.length
									? <div className='group-item flex-horizontal a-center j-center'>  <i className='fa fa-add'/> </div>
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
