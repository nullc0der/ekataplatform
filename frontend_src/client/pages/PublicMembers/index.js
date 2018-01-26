import React from 'react'
import classnames from 'classnames'
import request from 'superagent'
import { connect } from 'react-redux'
import _ from 'lodash'
import Helmet from 'react-helmet'
import withStyles from 'isomorphic-style-loader/lib/withStyles'

import { fetchUsers } from 'store/Users'
import { actions } from 'store/Chat'
import MemberTile from './MemberTile'
import s from './PublicMembers.styl'


class PublicMembers extends React.Component {

    state = {
        users: []
    }

    componentDidMount = () => {
        this.props.fetchUsers('/api/members/')
    }

    componentDidUpdate = (prevProps) => {
        if (
            prevProps.users !== this.props.users || 
            prevProps.onlineUsers !== this.props.onlineUsers ||
            prevProps.searchString !== this.props.searchString ||
            prevProps.filters !== this.props.filters
        ) {
            this.setUsers(
                this.props.users,
                this.props.onlineUsers,
                this.props.searchString,
                this.props.filters
            )
        }
    }

    chatButtonClicked = (e, id) => {
        e.preventDefault()
        const url = '/en/messaging/initmessage/' + id + '/?react=true'
        request
            .get(url)
            .end((err, res) => {
                if (res.ok) {
                    this.props.openMiniChat(res.body['id'])
                }
            })
    }

    setUsers = (users, onlineUsers, searchString='', filters=[]) => {
        let finalUsers = users.map(x => _.includes(onlineUsers, x.username)?{...x, is_online:true}: x)
        finalUsers = finalUsers.filter(x => x.username.toLowerCase().startsWith(searchString.toLowerCase()))
        if (!(_.includes(filters, 'staff') && _.includes(filters, 'member'))) {
            if (_.includes(filters, 'staff')) {
                finalUsers = finalUsers.filter(x => x.is_staff)
            }
            if (_.includes(filters, 'member')) {
                finalUsers = finalUsers.filter(x => !x.is_staff)
            }
        }
        if (!(_.includes(filters, 'online') && _.includes(filters, 'offline'))) {
            if (_.includes(filters, 'online')) {
                finalUsers = finalUsers.filter(x => x.is_online)
            }
            if (_.includes(filters, 'offline')) {
                finalUsers = finalUsers.filter(x => !x.is_online)
            }
        }
        this.setState({
            users: finalUsers
        })
    } 

    render() {
        const {
            className
        } = this.props

        const cx = classnames(s.container, className, 'flex-horizontal', 'flex-wrap', 'j-start', 'scroll-y')

        return (
            <div className={cx}>
                <Helmet title="Members" />
                {this.state.users.map((x, i) => 
                    <MemberTile
                        key={i}
                        userId={x.id}
                        userName={x.username}
                        fullName={x.fullname}
                        isOnline={x.is_online}
                        avatarUrl={x.user_image_url}
                        avatarColor={x.user_avatar_color}
                        publicURL={x.public_url}
                        isStaff={x.is_staff}
                        initChat={this.chatButtonClicked} />
                )}
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    users: state.Users.users,
    onlineUsers: state.Users.onlineUsers,
    searchString: state.Common.subHeaderSearchString,
    filters: state.Common.subHeaderFilters
})

const mapDispatchToProps = (dispatch) => ({
    fetchUsers: url => dispatch(fetchUsers(url)),
    openMiniChat: id => dispatch(actions.openMiniChat(id))
})

export default withStyles(s)(
    connect(mapStateToProps, mapDispatchToProps)(PublicMembers)
)
