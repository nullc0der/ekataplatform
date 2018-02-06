import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import request from 'superagent'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './SubHeader.styl'

import {connect} from 'react-redux'
import Link from 'react-router/lib/Link'

import startCase from 'lodash/startCase'
import take from 'lodash/take'

import Modal from 'components/ui/Modal'
import { actions } from 'store/Common'
import DropzoneWrapper from 'components/ui/DropzoneWrapper'
import SearchFilter from './SearchFilter'
import FILTERS from './filters'

class SubHeader extends Component {
	constructor(props) {
		super(props)
		this.state = {
			issueFormModalIsOpen: false,
			subject: '',
			description: '',
			subjectError: '',
			descriptionError: '',
			attachmentError: '',
			files: [],
			uploadPercent: 0,
			showSearchAndFilters: false,
			showFilterOptions: false,
			enabledFilters: ['online', 'offline', 'staff', 'member'],
			filters: ['online', 'offline', 'staff', 'member']
		}
	}

	componentDidMount = () => {
		this.setSearchAndFilters()
	}

	componentDidUpdate = (prevProps, prevState) => {
		if (prevProps.location.pathname !== this.props.location.pathname) {
			this.setSearchAndFilters()
		}
	}

	setSearchAndFilters = () => {
		const pathname = this.props.location.pathname.split('/').filter(x=>isNaN(x)).join('/')
		if (FILTERS[pathname]) {
			this.setState({
				showSearchAndFilters: true,
				enabledFilters: FILTERS[pathname].defaultFilters,
				filters: FILTERS[pathname].defaultFilters
			})
		} else {
			this.setState({
				showSearchAndFilters: false,
				enabledFilters: [],
				filters: []
			})
		}
	}

	toggleIssueModal = () => {
		this.setState(prevState => ({
			issueFormModalIsOpen: !prevState.issueFormModalIsOpen
		}))
	}

	handleIssueFormInputChange = (e) => {
		e.preventDefault()
		this.setState({
			[e.target.name]: e.target.value
		})
	}

	handleIssueFormSubmit = (e) => {
		e.preventDefault()
		const req = request
			.post('/postissue/')
			.set('X-CSRFToken', window.django.csrf)
			.field('subject', this.state.subject)
			.field('description', this.state.description)
		if (this.state.files.length) {
			this.state.files.map(f => {
				req.attach('attachments', f)
			})
			req.on('progress', event => {
				this.setState({
					uploadPercent: event.percent
				})
			})
		}
		req.end((err, res) => {
			if (!res.ok) {
				if (res.badRequest) {
					this.setState({
						subjectError: res.body.subject[0].message,
						descriptionError: res.body.description ? res.body.description[0].message : '',
						uploadPercent: 0
					})	
				} else {
					this.setState({
						attachmentError: res.text,
						uploadPercent: 0
					})
				}
				this.props.addNotification({
					message: 'Error Posting Issue',
					level: 'error'
				})
			} else {
				this.props.addNotification({
					message: 'Issue Posted Successfully',
					level: 'success'
				})
				this.setState({
					issueFormModalIsOpen: false,
					subject: '',
					description: '',
					subjectError: '',
					descriptionError: '',
					attachmentError: '',
					files: [],
					uploadPercent: 0
				})
			}
		})
	}

	onDrop = (acceptedFiles) => {
		this.setState({
			files: this.state.files ? this.state.files.concat(acceptedFiles) : acceptedFiles
		})
		if (this.state.files.length + acceptedFiles.length > 5) {
			this.setState({
				attachmentError: "You exceded total dropped file limit"
			})
		}
	}

	resetError = () => {
		if (this.state.files.length <= 5) {
			this.setState({
				attachmentError: ""
			})
		}
	}

	onTrashClick = (e, filename) => {
		e.stopPropagation()
		this.setState({
			files: this.state.files.filter(f => f.name !== filename)
		}, () => this.resetError())
	}

	toggleFilterOptions = (e) => {
		this.setState(prevState => ({
			showFilterOptions: !prevState.showFilterOptions
		}))
	}

	changeSearchString = (e) => {
		e.preventDefault()
		this.props.changeSearchString(e.target.value)
	}

	filterButtonClicked = (e) => {
		e.preventDefault()
		const prevFilters = this.state.enabledFilters
		let newFilters = _.includes(prevFilters, e.target.name)? prevFilters.filter(x => x!==e.target.name): prevFilters.concat(e.target.name)
		this.setState({
			enabledFilters: newFilters
		}, () => this.props.changeFilters(newFilters))
	}

	render(){
		const {
			className,
			location
		} = this.props;

		const cx = classnames(c.container, className, 'flex-horizontal', 'a-center')

		const paths = location.pathname.split('/').filter(x => !!x)
		const mainPath = startCase(paths[paths.length-1])

		const crumbs = paths.map((x,i) => {
			return {
				href: location.basename + take(paths, i+1).join('/'),
				text: startCase(x)
			}
		})

		return (
			<div className={cx} style={{ display: this.props.showHeaders ? 'flex' : 'none' }}>
				<div>
					<div className='title'> {mainPath} </div>
					<div className='list-links flex-horizontal'>
						{
							crumbs.map((x,i)=> {
								return <Link
									to={x.href}
									className='bread-link'
									key={i}> {x.text} {(crumbs.length - 1) !== i && '/'} </Link>
							})
						}
					</div>
				</div>
				<div className="flex-1"></div>
				{
					this.state.showSearchAndFilters &&
					<SearchFilter
						filters={this.state.filters}
						enabledFilters={this.state.enabledFilters}
						showFilterOptions={this.state.showFilterOptions}
						changeSearchString={this.changeSearchString}
						toggleFilterOptions={this.toggleFilterOptions}
						filterButtonClicked={this.filterButtonClicked} />
				}
				<button className="header-button" onClick={this.toggleIssueModal} title="Post an issue"><i className="fa fa-bug"></i></button>
				<Modal
					id="issue-form-modal"
					isOpen={this.state.issueFormModalIsOpen}
					title="Post an issue"
					onBackdropClick={this.toggleIssueModal}
					detachedFooter={true}
					detachedFooterText="Submit Issue"
					onDetachedFooterClick={this.handleIssueFormSubmit}
					uploadPercent={this.state.uploadPercent}>
					<form className="form-horizontal issue-form" onSubmit={this.handleIssueFormSubmit}>
						<div className={"form-group" + `${this.state.subjectError && " has-error"}`}>
							<label htmlFor="inputSubject" className="control-label">Subject</label>
							<input className="form-control" id="inputSubject" type="text"
								name="subject" value={this.state.subject} onChange={this.handleIssueFormInputChange} maxLength={200} />
							<small className="form-text">{this.state.subjectError}</small>
						</div>
						<div className={"form-group" + `${this.state.descriptionError && " has-error"}`}>
							<label htmlFor="inputDescription" className="control-label">Description</label>
							<textarea className="form-control" id="inputDescription" type="text"
								name="description" value={this.state.description} onChange={this.handleIssueFormInputChange} />
							<small className="form-text">{this.state.descriptionError}</small>
						</div>
						<div className="form-group">
							<DropzoneWrapper
								files={this.state.files}
								onDrop={this.onDrop}
								onTrashClick={this.onTrashClick}
								maxFile={5}
								hasError={this.state.attachmentError} />
							<small className="form-text">{this.state.attachmentError}</small>
						</div>
					</form>
				</Modal>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	location: state.router.locationBeforeTransitions
})

const mapDispatchToProps = (dispatch)=> ({
	addNotification: (notification) => dispatch(actions.addNotification(notification)),
	changeSearchString: (string) => dispatch(actions.changeSubHeaderSearchString(string)),
	changeFilters: (filters) => dispatch(actions.changeSubHeaderFilters(filters))
})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(SubHeader)
)
