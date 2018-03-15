import React from 'react'
import classnames from 'classnames'
import Helmet from 'react-helmet'

import NotificationCenter from 'components/NotificationCenter'
import GroupCard from './GroupCard'
import PostSection from './PostSection'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './PostPage.styl'


class PostPage extends React.Component {
    render() {
        const {
            className
        } = this.props

        const cx = classnames(c.container, className, 'flex-horizontal scroll-y')
        const notificationClass  = classnames(c.notifications, 'flex-1')
        const groupCardClass = classnames(c.groupcard)
        const postSectionClass = classnames(c.postsection, 'flex-1')
        return (
            <div className={cx}>
                <Helmet title={`Group | ${this.props.params.id} | Members`}/>
                <PostSection className={postSectionClass} groupID={this.props.params.id}/>
                <div className='boxes-in-right flex-vertical'>
                    <GroupCard
                        className={groupCardClass}
                        groupID={this.props.params.id}/>
                    <NotificationCenter
                        className={notificationClass}
                        groupID={this.props.params.id}/>
                </div>
            </div>
        )
    }
}

export default withStyles(c)(PostPage)
