import { Component } from 'react'
import classnames from 'classnames'

import Avatar from 'components/Avatar'


export default class MemberTile extends Component {
    render() {
        const {
            userId,
            userName,
            isOnline,
            avatarUrl,
            avatarColor,
            publicURL,
            isStaff,
            initChat
        } = this.props

        return (
            <div className={classnames("member-tile", {'is-online': isOnline})}>
                <a href={publicURL}>
                    <div className="member-image">
                        <p className="init-chat" onClick={(e) => initChat(e, userId)}><i className="fa fa-comments-o"></i></p>
                        {
                            avatarUrl ?
                                <img className='avatar-image rounded' src={avatarUrl} /> :
                                <Avatar className='avatar-image' name={userName} bgcolor={avatarColor} fontsize="2em" />
                        }
                    </div>
                    <div className={classnames("member-info", {'is-staff': isStaff})}>
                        <p className="username">{userName}</p>
                        <p className="status">{isStaff?'Staff':'Member'}</p>
                    </div>
                </a>
            </div>
        )
    }
}
