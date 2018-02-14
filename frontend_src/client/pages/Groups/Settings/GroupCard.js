import {Component} from 'react'
import classnames  from 'classnames'
import {connect} from 'react-redux'

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
			categoryDropdownVisible: false
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
				otherGroupType: this.groupTypes.indexOf(groupType) === -1 ? groupType : ""
			})
		}
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
			content
		)
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
				<div className='card-action'>
					{cardActionTexts[group.join_status]}
				</div>
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
