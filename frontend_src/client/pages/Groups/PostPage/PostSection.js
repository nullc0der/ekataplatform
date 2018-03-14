import React from 'react'
import { connect } from 'react-redux'
import classnames from 'classnames'
import request from 'superagent'
import _ from 'lodash'
import { Scrollbars } from 'react-custom-scrollbars'

import { actions as groupActions } from 'store/Groups'
import { actions as groupPostActions } from 'store/GroupPost'
import LoadingView from 'components/LoadingView'
import PostGroupCard from './PostGroupCard'
import PostEditor from './PostEditor'


class PostSectionCard extends React.Component {

    state = {
        posts : {}
    }

    componentDidMount = () => {
        const url = `/api/groups/posts/?groupID=${this.props.groupID}`
        this.props.fetchPosts(url)
        this.getGroupDetails()
    }

    componentDidUpdate = (prevProps, prevState) => {
        if (prevProps.posts !== this.props.posts) {
            this.setPosts(this.props.posts)
        }
    }

    getGroupDetails = () => {
        request
            .get(`/api/groups/${this.props.groupID}/details`)
            .end((err, res) => {
                if (res.ok) {
                    this.props.changeUserPermissionSetForGroup(res.body.user_permission_set)
                }
            })
    }

    setPosts = (fetchedPosts) => {
        this.setState({
            posts: _.groupBy(fetchedPosts, 'created_date')
        })
    }

    requestDeletePost = (e, postID) => {
        e.preventDefault()
        e.stopPropagation()
        const url = `/api/groups/posts/${postID}/`
        this.props.deletePost(url, postID)
    }

    requestApprovePost = (e, postID) => {
        e.preventDefault()
        e.stopPropagation()
        const url = `/api/groups/posts/${postID}/`
        this.props.approvePost(url)
    }

    requestDeleteComment = (e, commentID, postID) => {
        e.preventDefault()
        e.stopPropagation()
        const url = `/api/groups/posts/comment/${commentID}/`
        this.props.deleteComment(url, commentID, postID)
    }

    requestApproveComment = (e, commentID) => {
        e.preventDefault()
        e.stopPropagation()
        const url = `/api/groups/posts/comment/${commentID}/`
        this.props.approveComment(url)
    }

    render() {
          const {
            className,
            groupID,
            isLoading
          } = this.props

          const cx = classnames(className)

          return (
            <div className={cx}>
                {
                    isLoading ?
                    <LoadingView/> :
                    Object.keys(this.state.posts).reverse().map(
                        (date, i) => <PostGroupCard
                            key={i}
                            posts={this.state.posts[date]}
                            comments={this.props.comments}
                            date={date}
                            requestDeletePost={this.requestDeletePost}
                            requestApprovePost={this.requestApprovePost}
                            createComment={this.props.createComment}
                            getComments={this.props.fetchComments}
                            requestDeleteComment={this.requestDeleteComment}
                            requestApproveComment={this.requestApproveComment}
                            permissionSet={this.props.permissionSet}/>
                    )
                }
                <PostEditor createPost={this.props.createPost} groupID={groupID}/>
            </div>
          )
      }
 }

const mapStateToProps = (state) => ({
    isLoading: state.GroupPost.isLoading,
    posts: state.GroupPost.posts,
    comments: state.GroupPost.comments,
    permissionSet: state.Groups.userPermissionSetForViewingGroup
})

const mapDispatchToProps = (dispatch) => ({
    fetchPosts: (url) => dispatch(groupPostActions.getPosts(url)),
    createPost: (url, post, groupID) => dispatch(groupPostActions.createPost(url, post, groupID)),
    deletePost: (url, postID) => dispatch(groupPostActions.deletePost(url, postID)),
    approvePost: (url) => dispatch(groupPostActions.approvePost(url)),
    fetchComments: (url) => dispatch(groupPostActions.getComments(url)),
    createComment: (url, comment, postID) => dispatch(groupPostActions.createComment(url, comment, postID)),
    deleteComment: (url, commentID, postID) => dispatch(groupPostActions.deleteComment(url, commentID, postID)),
    approveComment: (url) => dispatch(groupPostActions.approveComment(url)),
    changeUserPermissionSetForGroup: (permissionSet) => dispatch(groupActions.changeUserPermissionSetForGroup(permissionSet))
})

export default connect(mapStateToProps, mapDispatchToProps)(PostSectionCard)
