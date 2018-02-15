import { Component } from 'react'
import classnames from 'classnames'
import {connect} from 'react-redux'
import Linkify from 'react-linkify'

import { actions as settingsActions } from 'store/GroupSettings'
import { actions as groupNotificationAction } from 'store/GroupNotifications'
import c from './Settings.styl'


class SettingsTabs extends Component {

    state = {
        clickedTab: 'General',
        joinStatusDropDownVisible: false,
        selectedStatus: 'request',
        approvePostChecked: false,
        approveCommentChecked: false,
        notificationInput: '',
        editingNotification: null
    }

    componentDidMount() {
        const id = this.props.groupID
        this.props.loadNotifications(`/api/groups/${id}/notifications/`)
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.group !== this.props.group) {
            this.setState({
                approveCommentChecked: this.props.group.auto_approve_comment,
                approvePostChecked: this.props.group.auto_approve_post,
                selectedStatus: this.props.group.join_status
            })
        }
    }

    sendDataToServer = () => {
        const id = this.props.groupID
        const content = {
            'from_settings': true,
            'auto_approve_post': this.state.approvePostChecked,
            'auto_approve_comment': this.state.approveCommentChecked,
            'join_status': this.state.selectedStatus.toLowerCase().trim()
        }
        this.props.editGroup(
            `/api/groups/${id}/settings/`,
            content
        )
    }

    createNotification = (e) => {
        e.preventDefault()
        const id = this.props.groupID
        if (this.state.notificationInput.length) {
            if (!this.state.editingNotification) {
                const payload = {
                    'notification': this.state.notificationInput
                }
                this.props.createNotification(
                    `/api/groups/${id}/notifications/`,
                    payload
                )   
            } else {
                const payload = {
                    'id': this.state.editingNotification,
                    'notification': this.state.notificationInput
                }
                this.props.updateNotification(
                    `/api/groups/${id}/notifications/`,
                    payload
                )
            }
            this.setState({
                notificationInput: '',
                editingNotification: null
            })
        }
    }

    deleteNotification = (e, id) => {
        e.preventDefault()
        this.props.deleteNotification(
            `/api/groups/${this.props.groupID}/notifications/`,
            id
        )
    }

    onNotificationInputChange = (e) => {
        e.preventDefault()
        this.setState({
            notificationInput: e.target.value
        })
    }

    onEditClick = (e, id, content) => {
        this.setState({
            editingNotification: id,
            notificationInput: content
        })
    }

    onCancelClick = (e) => {
        e.preventDefault()
        this.setState({
            editingNotification: null,
            notificationInput: ''
        })
    }

    onTabClick = (e, name) => {
        e.preventDefault()
        this.setState({
            clickedTab: name,
        })
    }

    onJoinStatusClick = (e) => {
        this.setState({
            joinStatusDropDownVisible: true
        })
    }

    onStatusOptionClick = (e, value) => {
        this.setState({
            selectedStatus: value,
            joinStatusDropDownVisible: false
        }, () => this.sendDataToServer())
    }

    onApprovePostClick = () => {
        this.setState(prevState => ({
            approvePostChecked: !prevState.approvePostChecked
        }), () => this.sendDataToServer())
    }

    onApproveCommentClick = () => {
        this.setState(prevState => ({
            approveCommentChecked: !prevState.approveCommentChecked
        }), () => this.sendDataToServer())
    }

    renderGeneralTab = () => {
        const selectOptions = [
            ['open', 'Open'],
            ['closed', 'Closed'],
            ['request', 'Request'],
            ['invite', 'Invite']
        ]

        const joinStatusInfo = {
            "open": "Anyone can join without approval",
            "closed": "Staff invitation only",
            "request": "Request to join group for approval",
            "invite": "Member invitation only"
        }

        return (
            <div className="content-wrapper">
                <div className="form-group">
                    <label htmlFor="inputJoinStatus" className="control-label">Join Status</label>
                    <input className="form-control" id="inputJoinStatus" type="text" value={this.state.selectedStatus}
                        readOnly={true}
                        name="join_status" onClick={this.onJoinStatusClick}/>
                    <ul className={`select-dropdown ${this.state.joinStatusDropDownVisible ? 'is-visible' : ''}`}>
                        {selectOptions.map(
                            (x, i) => <li
                                key={i}
                                className={`select-option ${this.state.selectedStatus === x[0] ? 'selected' : ''}`}
                                onClick={(e) => this.onStatusOptionClick(e, x[0])}>{x[1]}</li>
                        )}
                    </ul>
                    <div className='join-status-info'>{joinStatusInfo[this.state.selectedStatus]}</div>
                </div>
                <div className="form-group">
                    <input type="checkbox" name="approve_post" className="switch-input" checked={this.state.approvePostChecked} readOnly={true} />
                    <label className="switch-label" onClick={this.onApprovePostClick}>Auto approve post </label>
                </div>
                <div className="form-group">
                    <input type="checkbox" name="approve_post" className="switch-input" checked={this.state.approveCommentChecked} readOnly={true} />
                    <label className="switch-label" onClick={this.onApproveCommentClick}>Auto approve comment </label>
                </div>
            </div>
        )
    }

    renderNotificationTab = () => {
        return(
            <div className="content-wrapper">
                <div className="group-notifications">
                    {this.props.notifications.map((x, i) => {
                        return(
                            <div className="group-notification" key={i}>
                                <span>{new Date(x.created_on).toLocaleString()}</span>
                                <p><Linkify>{x.notification}</Linkify></p>
                                <div className="actions">
                                    <i className="material-icons" title="important">star_border</i>
                                    <i className="material-icons" title="edit" onClick={(e) =>  this.onEditClick(e, x.id, x.notification)}>mode_edit</i>
                                    <i className="material-icons" title="delete" onClick={(e) => this.deleteNotification(e, x.id)}>delete</i>
                                </div>
                            </div>
                        )
                    })}
                </div>
                <form className="flex-horizontal footer-form" onSubmit={this.createNotification}>
                    <div className="form-group flex-1">
                        <input
                            className="form-control"
                            type="text"
                            placeholder={this.state.editingNotification ? 'Edit notification' : 'Add a notification'}
                            value={this.state.notificationInput}
                            onChange={this.onNotificationInputChange} />
                    </div>
                    <button type="button" className={`btn btn-primary ${this.state.editingNotification ? 'shown': 'hidden'}`} onClick={this.onCancelClick}><i className="fa fa-times"></i></button>
                    <button className="btn btn-primary" onClick={this.createNotification}>Submit</button>
                </form>
            </div>
        )
    }

    render() {
        const {
            className,
            group
        } = this.props;

        const cx = classnames(c.container, 'ui-settings-card group-type-' + group.group_type.toLowerCase())
        return (
            <div className={cx}>
                <div className="card-header settings-header">
                    <div className="group-header-image" style={{ backgroundImage: `url(${group.header_image_url || ''})`, backgroundSize: 'cover' }}>
                    </div>
                    <h5>Settings</h5>
                    <div className="tabs">
                        <div className={`tab flex-1 ${this.state.clickedTab === 'General' && 'active'}`} onClick={(e) => this.onTabClick(e, 'General')}>General</div>
                        <div className={`tab flex-1 ${this.state.clickedTab === 'Notifications' && 'active'}`} onClick={(e) => this.onTabClick(e, 'Notifications')}>Notifications</div>
                    </div>
                </div>
                <div className="settings-content">
                    {this.state.clickedTab === 'General' && this.renderGeneralTab()}
                    {this.state.clickedTab === 'Notifications' && this.renderNotificationTab()}
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    group: state.GroupSettings.group,
    notifications: state.GroupNotifications.notifications
})

const mapDispatchToProps = (dispatch) => ({
    editGroup: (url, payload, logo = null, header = null) => dispatch(
        settingsActions.editGroup(url, payload, logo, header)),
    loadNotifications: (url) => dispatch(groupNotificationAction.loadNotifications(url)),
    createNotification: (url, payload) => dispatch(groupNotificationAction.createNotification(url, payload)),
    deleteNotification: (url, id) => dispatch(groupNotificationAction.deleteNotification(url, id)),
    updateNotification: (url, payload) => dispatch(groupNotificationAction.updateNotification(url, payload))
})

export default connect(mapStateToProps, mapDispatchToProps)(SettingsTabs)
