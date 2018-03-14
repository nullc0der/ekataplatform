import React from 'react'
import classnames from 'classnames'
import moment from 'moment'
import showdown from 'showdown'
import { Scrollbars } from 'react-custom-scrollbars'

import Avatar from 'components/Avatar'
import Modal from 'components/ui/Modal'


class PostGroupCard extends React.Component {

    state = {
        postModalIsShown: false,
        postInModal: {},
        commentInput: '',
        clickedOnPostAction: -1
    }

    shouldShowPostOptions = (post) => {
        if (this.props.permissionSet.indexOf(105) !== -1) {
            return true
        }
        if (post.creator.username === window.django.user.username) {
            return true
        }
        return false
    }

    componentDidUpdate = (prevProps, prevState) => {
        if (prevState.postInModal.id !== this.state.postInModal.id) {
            this.props.getComments(
                `/api/groups/posts/comment/?postID=${this.state.postInModal.id}`)
        }
        if (prevProps.comments !== this.props.comment) {
            if (this.commentScroller) {
                this.commentScroller.scrollToBottom()
            }
        }
    }

    convertMDToHtml = (md) => {
        const converter = new showdown.Converter({
            'noHeaderId': true,
            'simpleLineBreaks': true,
            'openLinksInNewWindow': true,
            'simplifiedAutoLink': true
        })
        return converter.makeHtml(md)
    }

    togglePostModal = (e) => {
        this.setState(prevState => ({
            postModalIsShown: !prevState.postModalIsShown
        }))
    }

    openPostModal = (e, post) => {
        this.setState({
            postModalIsShown: true,
            postInModal: post
        })
    }

    onChangeCommentInput = (e) => {
        this.setState({
            commentInput: e.target.value
        })
    }

    sendComment = (e, postID) => {
        e.preventDefault()
        if (this.state.commentInput.length) {
            this.props.createComment(
                '/api/groups/posts/comment/', this.state.commentInput, postID
            )
            this.setState({
                commentInput: ''
            })
        }
    }

    onPostActionClick = (e, postID) => {
        if (this.state.clickedOnPostAction === postID) {
            this.setState({
                clickedOnPostAction: -1
            })
        } else {
            this.setState({
                clickedOnPostAction: postID
            })
        }
    }

    renderOnePost = (post, i) => {
        return (
            <div className='post' key={i}>
                <div className='header'>
                    <div className='avatar'>
                        <a href={post.creator.profile.public_url} className="ui-avatar">
                          {
                              post.creator.profile.avatar.thumbnail ?
                                  <img className='img-responsive rounded' src={post.creator.profile.avatar.thumbnail} /> :
                                  <Avatar name={post.creator.fullname || post.creator.username} bgcolor={post.creator.profile.default_avatar_color} />
                          }
                        </a>
                    </div>
                    <div className='info'>
                        <span className='username'>{post.creator.username}</span>
                        <span className='time'>{moment(post.created_on).format('h:mm a')}</span>
                    </div>
                    <div className='flex-1'></div>
                    {!post.approved && <div className='status'>Pending Approval</div>}
                    {
                        this.shouldShowPostOptions(post) && 
                        <div className={`actions dropdown ${this.state.clickedOnPostAction === post.id && 'open'}`}>
                            <i className='fas fa-ellipsis-v' onClick={(e) => this.onPostActionClick(e, post.id)}></i>
                            <ul className='dropdown-menu animated fadeIn'>
                                {(this.props.permissionSet.indexOf(105) !== -1 & !post.approved) ?
                                    <li onClick={(e) => this.props.requestApprovePost(e, post.id)}><a href='#'>Approve</a></li> : ''
                                }
                                <li onClick={(e) => this.props.requestDeletePost(e, post.id)}><a href='#'>Delete</a></li>
                            </ul>
                        </div>
                    }
                </div>
                <div className='content' dangerouslySetInnerHTML={{ __html:  this.convertMDToHtml(post.post)}} onClick={(e) => this.openPostModal(e, post)}></div>
                <div className='footer'>
                  {/*<div className='social-buttons'>
                        <i className='fab fa-facebook'></i>
                        <i className='fab fa-twitter'></i>
                  </div>*/}
                  <div className='flex-1'></div>
                  <div className='comment-count'>
                        {post.comment_count !== 0 ? <p>{post.comment_count} comments</p> : ''}
                  </div>
                </div>
        </div>
        )
    }

    renderDetailPost = (post) => {
        return (
            <div className='post post-modal'>
                <div className='header'>
                    <div className='avatar'>
                        <a href={post.creator.profile.public_url} className="ui-avatar">
                          {
                              post.creator.profile.avatar.thumbnail ?
                                  <img className='img-responsive rounded' src={post.creator.profile.avatar.thumbnail} /> :
                                  <Avatar name={post.creator.fullname || post.creator.username} bgcolor={post.creator.profile.default_avatar_color} />
                          }
                        </a>
                    </div>
                    <div className='info'>
                        <span className='username'>{post.creator.username}</span>
                        <span className='time'>{moment(post.created_on).format('h:mm a')}</span>
                    </div>
                    <div className='flex-1'></div>
                    {!post.approved && <div className='status'>Pending Approval</div>}
                    {
                        this.shouldShowPostOptions(post) &&
                        <div className={`actions dropdown ${this.state.clickedOnPostAction === post.id && 'open'}`}>
                            <i className='fas fa-ellipsis-v' onClick={(e) => this.onPostActionClick(e, post.id)}></i>
                            <ul className='dropdown-menu animated fadeIn'>
                                {(this.props.permissionSet.indexOf(105) !== -1 & !post.approved) ?
                                    <li onClick={(e) => this.props.requestApprovePost(e, post.id)}><a href='#'>Approve</a></li> : ''
                                }
                                <li onClick={(e) => this.props.requestDeletePost(e, post.id)}><a href='#'>Delete</a></li>
                            </ul>
                        </div>
                    }
                </div>
                <div className='content' dangerouslySetInnerHTML={{ __html:  this.convertMDToHtml(post.post)}}></div>
                <div className='footer'>
                  <div className='comment-box'>
                    <Scrollbars autoHide autoHeight autoHeightMax={300} ref={node => {this.commentScroller = node}}>
                    {
                        this.props.comments.map(x => x.post.id === post.id ? <div className='comment' key={x.id}>
                            <div className='avatar'>
                                {
                                    x.commentor.profile.avatar.thumbnail ?
                                        <img className='img-responsive rounded' src={x.commentor.profile.avatar.thumbnail} /> :
                                        <Avatar name={x.commentor.fullname || x.commentor.username} bgcolor={x.commentor.profile.default_avatar_color} />
                                }
                            </div>
                            <div className='content'>
                                <p className='username'>{x.commentor.username}</p>
                                <p className='text'>{x.comment}</p>
                            </div>
                            {(!x.approved & this.props.permissionSet.indexOf(105) !== -1) ? <div 
                                className='status' title='approve'
                                onClick={(e) => this.props.requestApproveComment(e, x.id)}><i className='fas fa-check'></i></div> : ''}
                            {(this.props.permissionSet.indexOf(105) !== -1 | window.django.user.username === x.commentor.username) ?<div
                                className='status' title='delete'
                                onClick={(e) => this.props.requestDeleteComment(e, x.id)}><i className='fas fa-trash'></i></div> : ''}
                        </div> : '')
                    }
                    </Scrollbars>
                    <div className='comment'>
                        <div className='avatar'>
                            {
                                window.django.user.profile_image ?
                                    <img className='img-responsive rounded' src={window.django.user.profile_image} /> :
                                    <Avatar name={window.django.user.fullname || window.django.user.username} bgcolor={window.django.user.profile_avatar_color} />
                            }
                        </div>
                        <div className='comment-input-box'>
                            <form onSubmit={(e) => this.sendComment(e, post.id)}>
                                <input type='text' className='comment-input' value={this.state.commentInput} onChange={this.onChangeCommentInput} placeholder='press enter to post a comment'/>
                                <i className='fas fa-paper-plane' onClick={(e) => this.sendComment(e, post.id)}/>
                            </form>
                        </div>
                    </div>
                  </div>
                </div>
            </div>
        )
    }

    render() {
        const {
            className,
            date,
            posts,
            requestDeletePost,
            requestApprovePost
        } = this.props

        const cx = classnames(className, 'flex-vertical', 'post-group')

        return (
            <div className={cx}>
                <div className='date-area'>{moment(date).format("MMM Do, YYYY")}</div>
                <div className='ui-post-group-card'>
                    {posts.map(this.renderOnePost)}
                </div>
                <Modal isOpen={this.state.postModalIsShown} title='' id='postModal' onBackdropClick={this.togglePostModal}>
                    {this.state.postModalIsShown && this.renderDetailPost(this.state.postInModal)}
                </Modal>
            </div>
        )
    }
}

export default PostGroupCard
