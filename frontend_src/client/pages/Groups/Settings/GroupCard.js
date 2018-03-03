import {Component} from 'react'
import classnames  from 'classnames'
import {connect} from 'react-redux'
import request from 'superagent'
import Dropzone from 'react-dropzone'
import Modal from 'components/ui/Modal'

import {actions as settingsActions} from 'store/GroupSettings'
import {actions as groupActions} from 'store/Groups'

import c from './Settings.styl'

class GroupCard extends Component {
	constructor(props) {
		super(props)
		this.groupTypes = [
			"Art",
			"Activist",
			"Political",
			"News",
			"Business",
			"Government",
			"Blog",
			"Nonprofit Organization",
			"Other"
		]
		this.state = {
			otherGroupType: '',
			groupType: null,
			categoryDropdownVisible: false,
			logo: null,
			header: null,
			deleteGroupModalShown: false,
			flaggedForDelete: false,
			flaggedForDeleteOn: null
		}
	}

	componentDidMount() {
		const id = this.props.groupID
		this.props.loadGroup(`/api/groups/${id}/settings/`)
		this.props.changeLastGroup(id)
	}

	componentDidUpdate(prevProps) {
		if (prevProps.group !== this.props.group) {
			const groupType = this.props.group.group_type
			this.setState({
				groupType: this.groupTypes.indexOf(groupType) === -1 ? 9 : this.groupTypes.indexOf(groupType) + 1,
				otherGroupType: this.groupTypes.indexOf(groupType) === -1 ? groupType : "",
				flaggedForDelete: this.props.group.flagged_for_deletion,
				flaggedForDeleteOn: this.calculateDays(this.props.group.flagged_for_deletion_on)
			})
		}
	}

	calculateDays = (deleteDate) => {
		let days = null
		if(deleteDate) {
			const timeDiff = Math.abs(new Date(deleteDate).getTime() - new Date().getTime())
			days = Math.ceil(timeDiff / (1000 * 3600 * 24))
		}
		return days
	}

	onContentEditableBlurred = () => {
		const id = this.props.groupID
		const otherGroup = this.state.groupType === 9 ? this.state.otherGroupType : ""
		const content = {
			'name': this.nameEl.innerText.trim(),
			'short_about': this.sAboutEl.innerText.trim(),
			'long_about': this.lAboutEl.innerText.trim(),
			'group_type': this.state.groupType,
			'group_type_other': otherGroup
		}
		this.props.editGroup(
			`/api/groups/${id}/settings/`,
			content,
			this.state.logo ? this.state.logo[0] : null,
			this.state.header ? this.state.header[0] : null
		)
		this.setState({
			logo: null,
			header: null
		})
	}

	handleOtherTypeInputChange = (e) => {
		this.setState({
			otherGroupType: e.target.value
		})
	}

	toggleCategoryDropdown = () => {
		this.setState(prevState => ({
			categoryDropdownVisible: !prevState.categoryDropdownVisible
		}))
	}

	handleGroupTypeClick = (groupType) => {
		if (groupType === 9) {
			this.setState({
				groupType
			})
		} else {
			this.setState({
				groupType,
				categoryDropdownVisible: false
			}, () => this.onContentEditableBlurred())
		}
	}

	onOtherGroupTypeSubmit = (e) => {
		e.preventDefault()
		if (this.state.otherGroupType.length) {
			this.setState({
				categoryDropdownVisible: false
			}, () => this.onContentEditableBlurred())
		}
	}

	onDropLogo = (acceptedFile) => {
		this.setState({
			logo: acceptedFile
		}, () => this.onContentEditableBlurred())
	}

	onDropHeader = (acceptedFile) => {
		this.setState({
			header: acceptedFile
		}, () => this.onContentEditableBlurred())
	}

	toggleDeleteGroupModal = (e) => {
		this.setState(prevState => ({
			deleteGroupModalShown: !prevState.deleteGroupModalShown
		}))
	}

	handleConfirmDelete = (e) => {
		request
			.post(`/api/groups/${this.props.groupID}/requestdelete/`)
			.set('X-CSRFToken', window.django.csrf)
			.end((err, res) => {
				if (res.ok) {
					this.setState({
						flaggedForDelete: true,
						flaggedForDeleteOn: this.calculateDays(res.body)
					})
				}
			})
	}

	render(){
		const {
			className,
			groupID,
			group
		} = this.props

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

		const cardActionTexts = {
			"open": "Join Group",
			"closed": "Closed Group",
			"request": "Request to Join",
			"invite": "Invitation Only"
		}

		const cx = classnames(c.container, className, 'ui-group-card', 'group-type-' + group.group_type.toLowerCase())

		return (
			<div className={cx}>
				<div className='card-inner'>
					<div className='card-header flex-horizontal'>
						<div className="group-header-image" style={{ backgroundImage: `url(${group.header_image_url || ''})` }}>
							<Dropzone
								accept='image/*'
								multiple={false}
								className='dropzone' onDrop={this.onDropHeader}></Dropzone>
						</div>
						<div className="group-info">
							<div className='name'
								suppressContentEditableWarning={true}
								contentEditable={true}
								ref={(node) => {this.nameEl=node}}
								onBlur={this.onContentEditableBlurred}> {group.name} </div>
							<div className='category' onClick={this.toggleCategoryDropdown}> {group.group_type.split(" ").join("\n")} <i className="fa fa-caret-down"></i> </div>
						</div>
					</div>
					<ul className={`select-dropdown ${this.state.categoryDropdownVisible ? 'is-visible': ''}`}>
						{selectOptions.map(
							(x, i) => <li
								key={i}
								className={`select-option ${this.state.groupType === x[0] ? 'selected' : ''}`}
								onClick={() => this.handleGroupTypeClick(x[0])}>{x[1]}</li>
						)}
						{
							this.state.groupType === 9 &&
							<form onSubmit={this.onOtherGroupTypeSubmit}>
								<input type="text"
									className='form-control'
									placeholder="Please specify" value={this.state.otherGroupType} onChange={this.handleOtherTypeInputChange} />
							</form>
						}
					</ul>
					<div className='card-circle-image' style={{ backgroundImage: `url(${group.logo_url})` }}>
						<Dropzone accept='image/*' multiple={false} className='dropzone' onDrop={this.onDropLogo}></Dropzone>
					</div>

					<div className='card-body'>
						<h6> Short Description </h6>
						<p
							suppressContentEditableWarning={true}
							contentEditable={true}
							ref={(node) => { this.sAboutEl = node }}
							onBlur={this.onContentEditableBlurred}> {group.description} </p>

						<h6> Long Description </h6>
						<p
							suppressContentEditableWarning={true}
							contentEditable={true}
							ref={(node) => { this.lAboutEl = node }}
							onBlur={this.onContentEditableBlurred}> {group.ldescription} </p>


						<div className='bottom-stats flex-horizontal'>
							<div className='bottom-stat flex-1'>
								<div className='stat-value'> {group.members.length} </div>
								<div className='stat-label'> Members </div>
							</div>
							<div className='bottom-stat flex-1'>
								<div className='stat-value'> {group.subscribers.length} </div>
								<div className='stat-label'> Subscribers </div>
							</div>
							{/* <div className='bottom-stat flex-1'>
									<div className='stat-value'> {active} </div>
									<div className='stat-label'> Active </div>
								</div> */}
						</div>

					</div>
				</div>
				<div className='card-action' onClick={this.toggleDeleteGroupModal} style={{cursor: 'pointer'}}>
					{this.state.flaggedForDeleteOn ? 'Group will be deleted in ' + this.state.flaggedForDeleteOn + ' Day' : 'Delete this Group'}
				</div>
				<Modal
					id="deleteGroupModal"
					isOpen={this.state.deleteGroupModalShown}
					title="Delete group"
					onBackdropClick={this.toggleDeleteGroupModal}>
					<div className='delete-modal-content'>
						{
							!this.state.flaggedForDelete ?
							<div>
								<p>You are about to delete your group from this community<br />do you wish to archived your group ?</p>
								<div className="flex-horizontal btn-group">
									<button className='btn btn-yes flex-1' onClick={this.handleConfirmDelete}>Yes</button>
									<button className='btn btn-no flex-1' onClick={this.toggleDeleteGroupModal}>No</button>
								</div>
							</div> :
							<div>
								<p>Your group will be automatically removed in {this.state.flaggedForDeleteOn ? this.state.flaggedForDeleteOn : 30} days<br />
									if you did not wish to do this then you may contact<br />
									Ekata staff before it is removed permanently </p>
							</div>
						}
					</div>
				</Modal>
			</div>
		)
	}
}

const mapStateToProps = (state) => ({
	group: state.GroupSettings.group
})

const mapDispatchProps = (dispatch) => ({
	loadGroup: (url) => dispatch(settingsActions.loadGroup(url)),
	changeLastGroup: (id) => dispatch(groupActions.changeLastGroup(id)),
	editGroup: (url, payload, logo=null, header=null) => dispatch(
		settingsActions.editGroup(url, payload, logo, header))
})

export default connect(mapStateToProps, mapDispatchProps)(GroupCard)
