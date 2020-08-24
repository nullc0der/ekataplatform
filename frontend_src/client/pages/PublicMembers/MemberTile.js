import { Component } from 'react'
import classnames from 'classnames'

import Avatar from 'components/Avatar'


export default class MemberTile extends Component {

    handleHover = (e, entered) => {
        const element = e.target
        if (element.offsetWidth < element.scrollWidth) {
            $(element).find('.username').toggleClass('long')
        }
    }

    render() {
        const {
            userId,
            userName,
            fullName,
            isOnline,
            avatarUrl,
            avatarColor,
            publicURL,
            isStaff,
            initChat
        } = this.props

        return (
            <div className={classnames("member-tile", {'is-online': isOnline})} onMouseEnter={this.handleHover} onMouseLeave={this.handleHover}>
                <a href={publicURL}>
                    <div className="member-image">
                        <p className="init-chat" onClick={(e) => initChat(e, userId)}><i className="fa fa-comments-o"></i></p>
                        {
                            avatarUrl ?
                                <img className='avatar-image rounded' src={avatarUrl} /> :
                                <Avatar className='avatar-image' name={fullName || userName} bgcolor={avatarColor} fontsize="2em" />
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
