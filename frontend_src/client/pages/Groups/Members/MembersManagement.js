import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Members.styl'

import MemberItem from './MemberItem'

import {actions as memberActions} from 'store/Members'

class MembersManagement extends Component {
	renderOneMember = (member, i)=> {
		const {groups} = this.props;
		return <MemberItem
			key={i}
			groups={groups}
			name={member.name}
			memberId={member.id}
			toggleSubscribedGroup={this.props.toggleSubscribedGroup}
			subscribed_groups={member.subscribed_groups}
			status={member.status}/>
	}

	render(){
		const {
			className,
			list = []
		} = this.props;

		const cx = classnames(className, 'flex-vertical')

		return (
			<div className={cx}>
				<div className='panel-header'>
					<div className='header-inner'>
						<h4> Member Management </h4>
						<div className='members-searchbox-wrap'>
							<input
								type='text'
								placeholder='Search Users/Groups'
								className='form-control'/>
						</div>
					</div>
				</div>
				<div className='members-list'>
					{
						list.map(this.renderOneMember)
					}
				</div>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	list: state.Members.list,
	groups: state.Members.groups_list
})

const mapDispatchToProps = (dispatch)=> ({
	toggleSubscribedGroup(memberId, group){
		return dispatch(memberActions.toggleSubscribedGroup(memberId, group))
	}
})

export default connect(mapStateToProps,mapDispatchToProps)(MembersManagement)
