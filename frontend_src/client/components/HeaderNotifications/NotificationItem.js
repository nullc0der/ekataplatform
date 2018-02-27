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

    renderGroupInvite = (notification) => {
        const { isActive } = this.props

        const { actionButtonsRevealed, actionsVisible } = this.state
        return (
            <Swipeable className={`nc-list-item flex-horizontal a-center ${isActive ? 'active' : ''}`}
                onSwipedLeft={this.onSwipeLeft} onSwipedRight={this.onSwipeRight}>
                <a href={notification.sender.public_url}>
                    {
                        notification.sender.user_image_url ?
                            <img className='avatar-image rounded' src={notification.sender.user_image_url} /> :
                            <Avatar name={notification.sender.fullname || notification.sender.username} bgcolor={notification.sender.user_avatar_color} />
                    }
                </a>
                <div className='details'>
                    <div className='name'> {notification.sender.fullname || notification.sender.username} </div>
                    <div className='subtext'> Sent a invitation to group {notification.group.name} </div>
                </div>
                <div className={`actions ${actionsVisible ? 'visible' : ''}`}>
                    <div className='reveal-action-icon' onClick={this.onRevealActionClick}>
                        <i className={`fa fa-arrow-left ${actionButtonsRevealed ? 'reverse' : 'normal'}`}></i>
                    </div>
                    <div className={`buttons-container ${actionButtonsRevealed ? 'shown' : ''}`}>
                        <i
                            className='material-icons button'
                            title="accept"
                            onClick={(e) => this.props.acceptDenyInvite(e, notification.inviteid, true, notification.id)}>check</i>
                        <i
                            className='material-icons button'
                            title="deny"
                            onClick={(e) => this.props.acceptDenyInvite(e, notification.inviteid, false, notification.id)}>clear</i>
                    </div>
                </div>
            </Swipeable>
        )
    }


    render() {
        const { notification } = this.props

        let notificationElement = null
        switch(notification.type) {
            case 'groupinvite':
                notificationElement = this.renderGroupInvite(notification)
                break
        }

        return (
           notificationElement
        )
    }
}

export default NotificationItem
