import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import _ from 'lodash'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Groups.styl'

import {connect} from 'react-redux'
import {actions} from 'store/Groups'
import Modal from 'components/ui/Modal'
import GroupCard from './GroupCard'

class GroupsPage extends Component {

	state = {
		groups: [],
		createGroupModalIsOpen: false,
		inputFieldValues: {},
		inputFieldErrors: {}
	}

	componentDidMount = () => {
		this.props.loadGroups('/api/groups/')
	}

	componentDidUpdate = (prevProps) => {
		if (
			prevProps.groups !== this.props.groups ||
			prevProps.searchString !== this.props.searchString ||
			prevProps.filters !== this.props.filters
		) {
			this.setGroups(
				this.props.groups,
				this.props.searchString,
				this.props.filters
			)
		}
	}

	setGroups = (groups, searchString, filters) => {
		let finalGroups = groups.filter(x => x.name.toLowerCase().startsWith(searchString.toLowerCase()))
		let subscribedGroups = []
		let joinedGroups = []
		if (filters.length && !_.includes(filters, 'all')) {
			if (_.includes(filters, 'subscribed')) {
				subscribedGroups = finalGroups.filter(x => _.includes(x.subscribers, window.django.user.username))
			}
			if (_.includes(filters, 'joined')) {
				joinedGroups = finalGroups.filter(x => _.includes(x.members, window.django.user.username))
			}	
			finalGroups = _.union(subscribedGroups, joinedGroups)
		}
		this.setState({
			groups: finalGroups
		})
	}

	onSubscribeButtonClick = (e, groupID, subscribe=true) => {
		e.preventDefault()
		const url = `/api/groups/subscribe/${groupID}/`
		if (subscribe) {
			this.props.subscribeGroup(url)
		} else {
			this.props.unsubscribeGroup(url)
		}
	}

	toggleCreateGroupModal = (e) => {
		e.preventDefault()
		this.setState(prevState => ({
			createGroupModalIsOpen: !prevState.createGroupModalIsOpen
		}))
	}

	handleCreateGroupFormInputChange = (e) => {
		e.preventDefault()
		this.setState({
			inputFieldValues: {
				[e.target.name]: e.target.value
			}
		})
	}

	render(){
		const {
			className
		} = this.props;

		const cx = classnames(c.container, className)

		return (
			<div className={cx}>
				<div className="flex-horizontal j-end">
					<button className="btn btn-primary" onClick={this.toggleCreateGroupModal}><i className="fa fa-plus-circle"></i> Create Group</button>
				</div>
				{
					this.state.groups.map((x,i)=> {

						return <GroupCard
							key={i}
							id={x.id}
							groupURL={x.group_url}
							name={x.name}
							category={x.group_type}
							isSubscribed={_.includes(
									x.subscribers, window.django.user.username)}
							isMember={
								_.includes(
									x.members, window.django.user.username)
							}
							//headerURL={x.header_image_url}
							logoURL={x.logo_url}
							members={x.members.length}
							subscribers={x.subscribers.length}
							shortDescription={x.description}
							onSubscribeButtonClick={this.onSubscribeButtonClick}
							/>
					})
				}
				<Modal
					id="create-group-modal"
					isOpen={this.state.createGroupModalIsOpen}
					title="Create a group"
					onBackdropClick={this.toggleCreateGroupModal}
					detachedFooter={true}
					detachedFooterText="Create"
					onDetachedFooterClick={this.handleCreateGroupSubmit}>
					<form className="form-horizontal" style={{padding: '10px'}}>
						<div className={"form-group" + `${this.state.subjectError && " has-error"}`}>
							<label htmlFor="inputName" className="control-label">Name</label>
							<input className="form-control" id="inputName" type="text"
								name="name" value={this.state.inputFieldValues['name']} onChange={this.handleIssueFormInputChange}/>
							<small className="form-text"></small>
						</div>
					</form>
				</Modal>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	groups: state.Groups.groups,
	searchString: state.Common.subHeaderSearchString,
	filters: state.Common.subHeaderFilters
})

const mapDispatchToProps = (dispatch)=> ({
	loadGroups: (url) => dispatch(actions.loadGroups(url)),
	subscribeGroup: (url) => dispatch(actions.subscribeGroup(url)),
	unsubscribeGroup: (url) => dispatch(actions.unSubscribeGroup(url))
})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(GroupsPage)
)
