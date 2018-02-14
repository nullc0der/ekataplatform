import React from 'react'
import classnames from 'classnames'

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
                <GroupCard
                    groupID={this.props.params.id}/>
                <SettingsTabs
                    groupID={this.props.params.id}/>
            </div>
        )
    }
}

export default withStyles(c)(GroupSettings)
