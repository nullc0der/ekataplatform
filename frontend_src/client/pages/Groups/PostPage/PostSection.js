import React from 'react'
import { connect } from 'react-redux'
import classnames from 'classnames'

import { actions as groupPostActions } from 'store/GroupPost'
import PostGroupCard from './PostGroupCard'
import PostEditor from './PostEditor'


class PostSectionCard extends React.Component {

    createPost = (e, post) => {
        if (post.length) {
            const url = '/api/groups/posts/'
            this.props.createPost(url, post, this.props.groupID)
        }
    }

    render() {
          const {
            className,
            groupID
          } = this.props

          const cx = classnames(className, 'flex-vertical scroll-y')

          return (
            <div className={cx}>
                <PostGroupCard/>
                <PostEditor onClickSend={this.createPost}/>
            </div>
          )
      }
 }

const mapStateToProps = (state) => ({

})

const mapDispatchToProps = (dispatch) => ({
    createPost: (url, post, groupID) => dispatch(groupPostActions.createPost(url, post, groupID))
})

export default connect(mapStateToProps, mapDispatchToProps)(PostSectionCard)
