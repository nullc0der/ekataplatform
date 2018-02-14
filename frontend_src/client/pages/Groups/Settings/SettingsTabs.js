import { Component } from 'react'
import classnames from 'classnames'
import {connect} from 'react-redux'

import { actions as settingsActions } from 'store/GroupSettings'
import c from './Settings.styl'


class SettingsTabs extends Component {

    state = {
        clickedTab: 'General',
        joinStatusDropDownVisible: false,
        selectedStatus: 'request',
        approvePostChecked: false,
        approveCommentChecked: false
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
                    
                </div>
                <div className="form-group footer-form">
                    <input className="form-control" type="text"/>
                </div>
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
    group: state.GroupSettings.group
})

const mapDispatchToProps = (dispatch) => ({
    editGroup: (url, payload, logo = null, header = null) => dispatch(
        settingsActions.editGroup(url, payload, logo, header))
})

export default connect(mapStateToProps, mapDispatchToProps)(SettingsTabs)
