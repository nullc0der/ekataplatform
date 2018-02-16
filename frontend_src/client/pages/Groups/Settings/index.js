import React from 'react'
import classnames from 'classnames'
import Helmet from 'react-helmet'
import {connect} from 'react-redux'

import NotificationHeader from 'components/NotificationHeader'
import GroupCard from './GroupCard'
import SettingsTabs from './SettingsTabs'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './Settings.styl'


class GroupSettings extends React.Component {
    render() {
        const {
            className
        } = this.props;

        const cx = classnames(c.container, className)
        return (
            <div className={cx}>
                <Helmet title={`Groups | ${this.props.params.id} | Settings`} />
                {this.props.notifications.length > 0 && <NotificationHeader notifications={this.props.notifications}/>}
                <GroupCard
                    groupID={this.props.params.id}/>
                <SettingsTabs
                    groupID={this.props.params.id}/>
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    notifications: state.GroupNotifications.notifications
})

const mapDispatchToProps = (dispatch) => ({

})

export default withStyles(c)(
    connect(mapStateToProps, mapDispatchToProps)(GroupSettings))
