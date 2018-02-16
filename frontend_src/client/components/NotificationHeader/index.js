import React from 'react'
import classnames from 'classnames'
import Linkify from 'react-linkify'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './NotificationHeader.styl'


class NotificationHeader extends React.Component {

    state = {
        currentIndex: 0,
        notification: {}
    }

    componentDidMount() {
        if (this.props.notifications.length > 0) {
            this.setState({
                currentIndex: 0,
                notification: this.props.notifications[0]
            })
        }
    }

    onClickPrevious = (e) => {
        e.preventDefault()
        const {notifications} = this.props
        const {currentIndex} = this.state
        const nextIndex = currentIndex - 1
        if (nextIndex < 0) {
            this.setState({
                currentIndex: notifications.length - 1,
                notification: notifications[notifications.length - 1]
            })
        } else if (nextIndex > notifications.length - 1) {
            this.setState({
                currentIndex: 0,
                notification: notifications[0]
            })
        } else {
            this.setState({
                currentIndex: nextIndex,
                notification: notifications[nextIndex]
            })
        }
    }

    onClickNext = (e) => {
        e.preventDefault()
        const { notifications } = this.props
        const { currentIndex } = this.state
        const nextIndex = currentIndex + 1
        if (nextIndex < 0) {
            this.setState({
                currentIndex: notifications.length - 1,
                notification: notifications[notifications.length - 1]
            })
        } else if (nextIndex > notifications.length - 1) {
            this.setState({
                currentIndex: 0,
                notification: notifications[0]
            })
        } else {
            this.setState({
                currentIndex: nextIndex,
                notification: notifications[nextIndex]
            })
        }
    }

    render() {
        const {
            className
        } = this.props

        const { notification } = this.state
        const cx = classnames(c.container, className, 'flex-horizontal', {
            'is-important': notification.is_important
        })

        return (
            <div className={cx}>
                <i className="material-icons actions" onClick={this.onClickPrevious}>keyboard_arrow_left</i>
                <div className="content flex-1"><Linkify>{notification.notification}</Linkify></div>
                <div className="time">{new Date(notification.created_on).toLocaleString()}</div>
                <i className="material-icons actions" onClick={this.onClickNext}>keyboard_arrow_right</i>
            </div>
        )
    }
}

export default withStyles(c)(NotificationHeader)
