import React from 'react'
import classnames from 'classnames'
import moment from 'moment'
import showdown from 'showdown'

import Avatar from 'components/Avatar'


class PostGroupCard extends React.Component {

    convertMDToHtml = (md) => {
        const converter = new showdown.Converter()
        return converter.makeHtml(md)
    }

    render() {
        const {
            className,
            date,
            posts
        } = this.props

        const cx = classnames(className, 'flex-vertical', 'post-group')

        return (
            <div className={cx}>
                <div className='date-area'>{moment(date).format("MMM Do, YYYY")}</div>
                <div className='ui-post-group-card'>
                    {posts.map((post, i) => <div className='post' key={i}>
                        <div className='header'>
                            <div className='avatar'>
                                <a href={post.creator.profile.public_url} className="ui-avatar">
                                  {
                                      post.creator.profile.avatar.thumbnail ?
                                          <img className='img-responsive rounded' src={post.creator.profile.avatar.thumbnail} /> :
                                          <Avatar name={post.creator.username} bgcolor={user.creator.profile.default_avatar_color} />
                                  }
                                </a>
                            </div>
                            <div className='info'>
                                <span className='username'>{post.creator.username}</span>
                                <span className='time'>{moment(post.created_on).format('h:mm a')}</span>
                            </div>
                            <div className='flex-1'></div>
                            {!post.approved && <div className='status'>Pending Approval</div>}
                            <div className='actions dropdown'>
                                <i className='fas fa-ellipsis-v'></i>
                                <ul className="dropdown-menu animated fadeIn">
                                    <li><a href='#'>Delete Message</a></li>
                                    <li><a href='#'>Approve</a></li>
                                </ul>
                            </div>
                        </div>
                        <div className='content' dangerouslySetInnerHTML={{ __html:  this.convertMDToHtml(post.post)}}></div>
                        <div className='footer'>
                          {/*<div className='social-buttons'>
                                <i className='fab fa-facebook'></i>
                                <i className='fab fa-twitter'></i>
                          </div>*/}
                          <div className='flex-1'></div>
                          <div className='comment-count'>
                                <p>{post.comment_count} comments</p>
                          </div>
                        </div>
                    </div>)}
                </div>
            </div>
        )
    }
}

export default PostGroupCard
