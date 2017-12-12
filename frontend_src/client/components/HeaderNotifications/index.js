import {Component} from 'react'
import classnames  from 'classnames'


import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './HeaderNotifications.styl'

import Dropdown from 'components/ui/Dropdown'

import SAMPLE_NOTIFICATIONS from './sample-list'

class HeaderNotifications extends Component {

    state = {
        list: [],
        isOpen: false
    }

    componentDidMount = ()=> {
        this.fetchNotifications()
            .then(list => this.setState({list}))
            .catch(err => this.setState({hasError: err.message }))
    }

    fetchNotifications = ()=> {
        this.setState({isLoading: true, hasError: false})
        return Promise.resolve(
            SAMPLE_NOTIFICATIONS
        )
    }

    toggleOpen = ()=> {
        this.setState({isOpen: !this.state.isOpen})
    }

    renderOneNotication = (item, i)=> {

        return (
            <div
                key={i}
                className='notification-item flex-horizontal'>
                <div className='notification-icon black-bg'>
                    <img className='img-responsive'/>
                </div>
                <div className='flex-1'>
                    <div className='notification-title'>
                        {item.title}
                    </div>
                    <div className='notification-desc'>
                        {item.desc}
                    </div>
                </div>
            </div>
        )
    }

    render(){
        const {className} = this.props;
        const {list} = this.state;
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
                items={list}
                dropdownFooter={dropdownFooter}
                itemRenderer={this.renderOneNotication}/>
        )
    }
}

export default withStyles(c)(HeaderNotifications)
