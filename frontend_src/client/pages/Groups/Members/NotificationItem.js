import React from 'react'

import Linkify from 'react-linkify'
import Swipeable from 'react-swipeable'


class NotificationItem extends React.Component {

    state = {
        actionButtonsRevealed: false,
        actionsVisible: false
    }

    onRevealActionClick = (e) => {
        this.setState(prevState => ({
            actionButtonsRevealed: !prevState.actionButtonsRevealed
        }))
    }

    onSwipeLeft = (e) => {
        this.setState({
            actionButtonsRevealed: true,
            actionsVisible: true
        })
    }

    onSwipeRight = (e) => {
        this.setState({
            actionButtonsRevealed: false,
            actionsVisible: false
        })
    }

    render() {
        const { notification } = this.props

        const { actionButtonsRevealed, actionsVisible } = this.state

        return (
            <Swipeable className='nc-list-item flex-horizontal a-center'
                onSwipedLeft={this.onSwipeLeft} onSwipedRight={this.onSwipeRight}>
                <div className='details'>
                    <div className='name'><Linkify>{notification.notification}</Linkify></div>
                    <div className='subtext'>{new Date(notification.created_on).toLocaleString()}</div>
                </div>
                <div className={`actions ${actionsVisible? 'visible': ''}`}>
                    <div className='reveal-action-icon' onClick={this.onRevealActionClick}>
                        <i className={`fa fa-arrow-left ${actionButtonsRevealed ? 'reverse': 'normal'}`}></i>
                    </div>
                    <div className={`buttons-container ${actionButtonsRevealed ? 'shown': ''}`}>
                        <i className='material-icons button'>check</i>
                        <i className='material-icons button'>chat</i>
                    </div>
                </div>
            </Swipeable>
        )
    }
}

export default NotificationItem
