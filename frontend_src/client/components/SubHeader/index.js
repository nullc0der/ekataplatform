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

class SubHeader extends Component {
	constructor(props) {
		super(props)
		this.state = {
			issueFormModalIsOpen: false,
			subject: '',
			description: '',
			subjectError: '',
			descriptionError: ''
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

	handleIssueFormSubmit = () => {
		request
			.post('/postissue/')
			.type('form')
			.set('X-CSRFToken', window.django.csrf)
			.send({
				subject: this.state.subject,
				description: this.state.description
			})
			.end((err, res) => {
				if (!res.ok) {
					this.setState({
						subjectError: res.body.subject[0].message,
						descriptionError: res.body.description ? res.body.description[0].message : ''
					})
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
						descriptionError: ''
					})
				}
			})
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

		// console.log(paths)

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
				<div>
					<button className="btn btn-default" onClick={this.toggleIssueModal}><i className="fa fa-bug"></i> Post an issue</button>
				</div>
				<Modal
					id="issue-form-modal"
					isOpen={this.state.issueFormModalIsOpen}
					title="Post an issue"
					onBackdropClick={this.toggleIssueModal}
					detachedFooter={true}
					detachedFooterText="Submit Issue"
					onDetachedFooterClick={this.handleIssueFormSubmit}>
					<form className="form-horizontal issue-form">
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
	addNotification: (notification) => dispatch(actions.addNotification(notification))
})

export default withStyles(c)(
	connect(mapStateToProps,mapDispatchToProps)(SubHeader)
)
