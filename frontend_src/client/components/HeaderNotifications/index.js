import {Component} from 'react'
import classnames  from 'classnames'
import { connect } from 'react-redux'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './HeaderNotifications.styl'

import Dropdown from 'components/ui/Dropdown'
import NotificationItem from './NotificationItem'
import { actions as userNotificationsActions } from 'store/UserNotifications'

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
                setActiveNode={this.setActiveNode} />
        )
    }

    render(){
        const {className, notifications} = this.props;
        const cx = classnames(c.container, className)

        const listClass = classnames('notification-list', {
            'is-open': this.state.isOpen
        })

        const label = (
            <span className='notification-label'>
                <i className='fa fa-fw fa-bell-o'/>
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
                dropdownFooter={dropdownFooter}
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
    }
})

export default withStyles(c)(
    connect(mapStateToProps, mapDispatchToProps)(HeaderNotifications)
)
