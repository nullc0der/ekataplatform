import React from 'react'

import Linkify from 'react-linkify'
import Swipeable from 'react-swipeable'

import Avatar from 'components/Avatar'


class NotificationItem extends React.Component {

    state = {
        actionButtonsRevealed: false,
        actionsVisible: false
    }

    onRevealActionClick = (e) => {
        this.setState(prevState => ({
            actionButtonsRevealed: !prevState.actionButtonsRevealed,
            actionsVisible: false
        }))
    }

    onSwipeLeft = (e) => {
        this.setState({
            actionButtonsRevealed: true,
            actionsVisible: true
        }, () => this.props.setActiveNode(this.props.notification.id))
    }

    onSwipeRight = (e) => {
        this.setState({
            actionButtonsRevealed: false,
            actionsVisible: false
        })
    }

    renderGroupNotification = (notification) => {
        const { isActive } = this.props

        const { actionButtonsRevealed, actionsVisible } = this.state
        return (
            <Swipeable className={`nc-list-item flex-horizontal a-center ${isActive ? 'active' : ''}`}
                onSwipedLeft={this.onSwipeLeft} onSwipedRight={this.onSwipeRight}>
                {
                    notification.basic_group.logo_url ?
                        <img className='avatar-image rounded' src={notification.basic_group.logo_url} /> :
                        <Avatar name={notification.basic_group.name} />
                }
                <div className='details'>
                    <div className='name'><Linkify>{notification.notification}</Linkify></div>
                    <div className='subtext'>{new Date(notification.created_on).toLocaleString()}</div>
                </div>
                <div className={`actions ${actionsVisible ? 'visible' : ''}`}>
                    <div className='reveal-action-icon' onClick={this.onRevealActionClick}>
                        <i className={`fa fa-arrow-left ${actionButtonsRevealed ? 'reverse' : 'normal'}`}></i>
                    </div>
                    <div className={`buttons-container ${actionButtonsRevealed ? 'shown' : ''}`}>
                        <i className='material-icons button' title="mark as read"
                            onClick={() => this.props.setNotificationRead(notification.notification_id)}>check</i>
                    </div>
                </div>
            </Swipeable>
        )
    }

    renderJoinRequest = (notification) => {
        const { isActive } = this.props

        const { actionButtonsRevealed, actionsVisible } = this.state
        return (
            <Swipeable className={`nc-list-item flex-horizontal a-center ${isActive ? 'active' : ''}`}
                onSwipedLeft={this.onSwipeLeft} onSwipedRight={this.onSwipeRight}>
                <a href={notification.user.public_url}>
                    {
                        notification.user.avatar_url ?
                            <img className='avatar-image rounded' src={notification.user.avatar_url} /> :
                            <Avatar name={notification.user.fullname || notification.user.username} bgcolor={notification.user.user_avatar_color} />
                    }
                </a>
                <div className='details'>
                    <div className='name'> {notification.user.fullname || notification.user.username} </div>
                    <div className='subtext'> Sent a request to join to group {notification.groupname} </div>
                </div>
                <div className={`actions ${actionsVisible ? 'visible' : ''}`}>
                    <div className='reveal-action-icon' onClick={this.onRevealActionClick}>
                        <i className={`fa fa-arrow-left ${actionButtonsRevealed ? 'reverse' : 'normal'}`}></i>
                    </div>
                    <div className={`buttons-container ${actionButtonsRevealed ? 'shown' : ''}`}>
                        <i
                            className='material-icons button'
                            title="accept"
                            onClick={() => this.props.acceptDenyJoinRequest(notification.notification_id, notification.joinrequest_id, true)}>group_add</i>
                        <i
                            className='material-icons button'
                            title="deny"
                            onClick={() => this.props.acceptDenyJoinRequest(notification.notification_id, notification.joinrequest_id, false)}>clear</i>
                    </div>
                </div>
            </Swipeable>
        )
    }


    render() {
        const { notification } = this.props

        let notificationElement = null
        switch(notification.type) {
            case 'groupnotification':
                notificationElement = this.renderGroupNotification(notification)
                break
            case 'joinrequest':
                notificationElement = this.renderJoinRequest(notification)
                break
        }

        return (
           notificationElement
        )
    }
}

export default NotificationItem
