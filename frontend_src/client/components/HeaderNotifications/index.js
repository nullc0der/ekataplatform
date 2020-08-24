import {Component} from 'react'
import classnames  from 'classnames'
import { connect } from 'react-redux'
import request from 'superagent'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './HeaderNotifications.styl'

import Dropdown from 'components/ui/Dropdown'
import NotificationItem from './NotificationItem'
import { actions as userNotificationsActions } from 'store/UserNotifications'
import { actions as commonActions } from 'store/Common'

class HeaderNotifications extends Component {

    state = {
        isOpen: false,
        activeNode: null
    }

    componentDidMount = ()=> {
       this.props.fetchNotifications(
           '/api/notification/'
       )
    }

    toggleOpen = ()=> {
        this.setState({isOpen: !this.state.isOpen})
    }

    setActiveNode = (id) => {
        this.setState({
            activeNode: id
        })
    }

    renderOneNotication = (x, i)=> {
        return (
            <NotificationItem
                key={i} notification={x} isActive={this.state.activeNode === x.id}
                setActiveNode={this.setActiveNode}
                acceptDenyInvite={this.acceptDenyInvite} />
        )
    }

    acceptDenyInvite = (e, inviteID, accepted, notificationID) => {
        request
            .post(`/api/groups/acceptinvite/`)
            .set('X-CSRFToken', window.django.csrf)
            .send({ 'invite_id': inviteID, 'accepted': accepted })
            .end((err, res) => {
                if (res.ok) {
                    this.props.removeNotification(notificationID)
                    this.props.addNotification({
                        'message': res.body.message,
                        'level': 'success'
                    })
                }
            })
    }

    render(){
        const {className, notifications} = this.props;
        const cx = classnames(c.container, className)

        const listClass = classnames('notification-list', {
            'is-open': this.state.isOpen
        })

        const label = (
            <span className='notification-label'>
                <i className='far fa-fw fa-bell'/>
                {notifications.length ? <i className='has-notification'></i>: ''}
            </span>
        )

        const dropdownFooter = (
            <div className='flex-1 text-center mark-read-btn'>
                Mark all as Read
            </div>
        )

        return (
            <Dropdown
                id='id-header-mini-notifications'
                className={cx}
                label={label}
                items={notifications}
                itemRenderer={this.renderOneNotication}/>
        )
    }
}

const mapStateToProps = (state) => ({
    notifications: state.UserNotifications.notifications
})

const mapDispatchToProps = (dispatch) => ({
    fetchNotifications: (url) => {
        dispatch(userNotificationsActions.fetchNotifications(url))
    },
    removeNotification: (id) => {
        dispatch(userNotificationsActions.removeNotification(id))
    },
    addNotification: (notification) => {
        dispatch(commonActions.addNotification(notification))
    }
})

export default withStyles(c)(
    connect(mapStateToProps, mapDispatchToProps)(HeaderNotifications)
)
