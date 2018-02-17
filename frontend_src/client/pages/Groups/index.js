import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import _ from 'lodash'
import request from 'superagent'
import Helmet from 'react-helmet'

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
		inputFieldValues: {
			name: '',
			short_about: '',
			group_type: [],
			other: ''
		},
		inputFieldErrors: {},
		selectInputFocused: false,
		creatingGroup: false
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
		finalGroups.sort(
			(a, b) => { return _.includes(b.members, window.django.user.username) - _.includes(a.members, window.django.user.username) }
		)
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
		if (!this.state.creatingGroup) {
			this.setState(prevState => ({
				createGroupModalIsOpen: !prevState.createGroupModalIsOpen
			}))	
		}
	}

	handleCreateGroupFormInputChange = (e) => {
		e.preventDefault()
		this.setState({
			inputFieldValues: {
				...this.state.inputFieldValues,
				[e.target.name]: e.target.value
			}
		})
	}

	handleSelectFocus = (e) => {
		e.preventDefault()
		e.target.blur()
		this.setState(prevState => ({
			selectInputFocused: !prevState.selectInputFocused
		}))
	}

	handleOptionSelect = (id, value) => {
		this.setState({
			inputFieldValues: {
				...this.state.inputFieldValues,
				group_type: [id, value]
			},
			selectInputFocused: false
		})
	}

	handleCreateGroupSubmit = (e) => {
		e.preventDefault()
		this.setState({
			creatingGroup: true
		})
		request
			.post('/api/groups/create/')
			.set('X-CSRFToken', window.django.csrf)
			.send({
				name: this.state.inputFieldValues['name'],
				short_about: this.state.inputFieldValues['short_about'],
				group_type: this.state.inputFieldValues['group_type'][0],
				group_type_other: this.state.inputFieldValues['group_type'][1] === "Other" ? this.state.inputFieldValues['other'] : ""
			})
			.end((err, res) => {
				if (err && err.status === 400) {
					this.setState({
						inputFieldErrors: JSON.parse(res.body),
						creatingGroup: false
					})
				} else {
					if (res.ok) {
						this.props.groupCreated(res.body)
					}
					this.setState({
						inputFieldErrors: {},
						inputFieldValues: {
							name: '',
							short_about: '',
							group_type: [],
							other: ''
						},
						createGroupModalIsOpen: false,
						creatingGroup: false
					})
				}
			})
	}

	handleJoinGroup = (e, groupID, type) => {
		e.preventDefault()
		this.props.joinGroup(groupID, type)
	}

	render(){
		const {
			className
		} = this.props;

		const cx = classnames(c.container, className)
		const selectOptions = [
			[1, "Art"],
			[2, "Activist"],
			[3, "Political"],
			[4, "News"],
			[5, "Business"],
			[6, "Government"],
			[7, "Blog"],
			[8, "Nonprofit Organaization"],
			[9, "Other"]
		]

		return (
			<div className={cx}>
				<Helmet title="Community | Groups" />
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
							joinRequestSent={x.joinrequest_sent}
							headerURL={x.header_image_url}
							logoURL={x.logo_url}
							members={x.members.length}
							subscribers={x.subscribers.length}
							shortDescription={x.description}
							joinStatus={x.join_status}
							onSubscribeButtonClick={this.onSubscribeButtonClick}
							onJoinButtonClick={this.handleJoinGroup}
							/>
					})
				}
				<Modal
					id="create-group-modal"
					isOpen={this.state.createGroupModalIsOpen}
					title="Create a group"
					onBackdropClick={this.toggleCreateGroupModal}
					detachedFooter={true}
					detachedFooterText={this.state.creatingGroup? "Creating...": "Create"}
					onDetachedFooterClick={this.handleCreateGroupSubmit}>
					<form className="form-horizontal" style={{ padding: '10px' }} onSubmit={this.handleCreateGroupSubmit}>
						<div className={`form-group ${this.state.inputFieldErrors["name"] ? 'has-error': ''}`}>
							<input className={`form-control ${this.state.inputFieldValues['name'] ? 'has-value' : ''}`} id="inputName" type="text"
								name="name" value={this.state.inputFieldValues['name']} onChange={this.handleCreateGroupFormInputChange}
								autoComplete="off"/>
							<label htmlFor="inputName" className="control-label">Name</label>
							<small className="form-text">{this.state.inputFieldErrors["name"] && this.state.inputFieldErrors["name"][0].message}</small>
						</div>
						<div className={`form-group ${this.state.inputFieldErrors["short_about"] ? 'has-error' : ''}`}>
							<input className={`form-control ${this.state.inputFieldValues['short_about'] ? 'has-value' : ''}`}  id="inputSAbout" type="text"
								name="short_about" value={this.state.inputFieldValues['short_about']} onChange={this.handleCreateGroupFormInputChange}
								autoComplete="off" />
							<label htmlFor="inputSAbout" className="control-label">Short About</label>
							<small className="form-text">{this.state.inputFieldErrors["short_about"] && this.state.inputFieldErrors["short_about"][0].message}</small>
						</div>
						<div className={`form-group ${this.state.inputFieldErrors["group_type"] ? 'has-error' : ''}`}>
							<input className={`form-control ${this.state.inputFieldValues['group_type'][1] ? 'has-value' : ''}`}
								   id="inputGroupType" type="text"
								   onFocus={this.handleSelectFocus}
								   value={this.state.inputFieldValues['group_type'][1] || ""} 
								   autoComplete="off"/>
							<label htmlFor="inputGroupType" className="control-label">Group Type</label>
							<small className="form-text">{this.state.inputFieldErrors["group_type"] && this.state.inputFieldErrors["group_type"][0].message}</small>
							<ul className={`select-dropdown ${this.state.selectInputFocused ? 'is-visible' : ''}`}>
								<li className="select-option" onClick={() => this.handleOptionSelect('', '')}>---------</li>
								{selectOptions.map(
									(x, i) => <li 
										key={i}
										className={`select-option ${this.state.inputFieldValues['group_type'][1] === x[1] && 'selected'}`}
										onClick={() => this.handleOptionSelect(x[0], x[1])}>{x[1]}</li>
								)}
							</ul>
						</div>
						{
							this.state.inputFieldValues['group_type'][1] === 'Other' &&
							<div className={`form-group ${this.state.inputFieldErrors["group_type_other"] ? 'has-error' : ''}`}>
								<input className={`form-control ${this.state.inputFieldValues['other'] ? 'has-value' : ''}`} id="inputOther" type="text"
									name="other" value={this.state.inputFieldValues['other']} onChange={this.handleCreateGroupFormInputChange}
									autoComplete="off" />
								<label htmlFor="inputOther" className="control-label">Please Specify</label>
								<small className="form-text">{this.state.inputFieldErrors["group_type_other"] && this.state.inputFieldErrors["group_type_other"][0].message}</small>
							</div>
						}
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
	unsubscribeGroup: (url) => dispatch(actions.unSubscribeGroup(url)),
	groupCreated: (group) => dispatch(actions.groupCreated(group)),
	joinGroup: (groupID, type) => dispatch(actions.joinGroup(groupID, type))
})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(GroupsPage)
)
