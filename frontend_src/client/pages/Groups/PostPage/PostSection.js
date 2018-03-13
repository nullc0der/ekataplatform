import React from 'react'
import { connect } from 'react-redux'
import classnames from 'classnames'
import _ from 'lodash'
import { Scrollbars } from 'react-custom-scrollbars'

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
    }

    componentDidUpdate = (prevProps, prevState) => {
        if (prevProps.posts !== this.props.posts) {
            this.setPosts(this.props.posts)
        }
    }

    setPosts = (fetchedPosts) => {
        this.setState({
            posts: _.groupBy(fetchedPosts, 'created_date')
        })
    }

    render() {
          const {
            className,
            groupID,
            isLoading
          } = this.props

          const cx = classnames(className, 'flex-vertical')

          return (
            <div className={cx}>
                {
                    isLoading ?
                    <LoadingView/> :
                    Object.keys(this.state.posts).reverse().map(
                        (date, i) => <PostGroupCard key={i} posts={this.state.posts[date]} date={date}/>
                    )
                }
                <PostEditor createPost={this.props.createPost} groupID={groupID}/>
            </div>
          )
      }
 }

const mapStateToProps = (state) => ({
    isLoading: state.GroupPost.isLoading,
    posts: state.GroupPost.posts
})

const mapDispatchToProps = (dispatch) => ({
    fetchPosts: (url) => dispatch(groupPostActions.getPosts(url)),
    createPost: (url, post, groupID) => dispatch(groupPostActions.createPost(url, post, groupID))
})

export default connect(mapStateToProps, mapDispatchToProps)(PostSectionCard)
