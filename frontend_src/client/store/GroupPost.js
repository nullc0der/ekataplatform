import request from 'superagent'


const INITIAL_STATE = {
    posts: [],
    comments: [],
    isLoading: false,
    editingPost: -1
}


const POSTS_ARE_LOADING = 'POSTS_ARE_LOADING'
const postsAreLoading = (status) => ({
    type: POSTS_ARE_LOADING,
    status
})


const POST_LOAD_SUCCESS = 'POST_LOAD_SUCCESS'
const postLoadSuccess = (posts) => ({
    type: POST_LOAD_SUCCESS,
    posts
})

const ADD_SINGLE_POST = 'ADD_SINGLE_POST'
const addSinglePost = (post) => ({
    type: ADD_SINGLE_POST,
    post
})

const DELETE_SINGLE_POST = 'DELETE_SINGLE_POST'
const deleteSinglePost = (postID) => ({
    type: DELETE_SINGLE_POST,
    postID
})

const UPDATE_SINGLE_POST = 'UPDATE_SINGLE_POST'
const updateSinglePost = (post) => ({
    type: UPDATE_SINGLE_POST,
    post
})

const COMMENT_LOAD_SUCCESS = 'COMMENT_LOAD_SUCCESS'
const commentLoadSuccess = (comments) => ({
    type: COMMENT_LOAD_SUCCESS,
    comments
})

const ADD_SINGLE_COMMENT = 'ADD_SINGLE_COMMENT'
const addSingleComment = (comment) => ({
    type: ADD_SINGLE_COMMENT,
    comment
})

const DELETE_SINGLE_COMMENT = 'DELETE_SINGLE_COMMENT'
const deleteSingleComment = (commentID) => ({
    type: DELETE_SINGLE_COMMENT,
    commentID
})

const UPDATE_SINGLE_COMMENT = 'UPDATE_SINGLE_COMMENT'
const updateSingleComment = (comment) => ({
    type: UPDATE_SINGLE_COMMENT,
    comment
})

const UPDATE_COMMENT_COUNT = 'UPDATE_COMMENT_COUNT'
const updateCommentCount = (postID, negative=false) => ({
    type: UPDATE_COMMENT_COUNT,
    postID,
    negative
})

const UPDATE_EDITING_POST = 'UPDATE_EDITING_POST'
const updateEditingPost = (postID) => ({
    type: UPDATE_EDITING_POST,
    postID
})


const getPosts = (url) => {
    return (dispatch) => {
        dispatch(postsAreLoading(true))
        request
            .get(url)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(postLoadSuccess(res.body))
                    dispatch(postsAreLoading(false))
                } else {
                    dispatch(postsAreLoading(false))
                }
            })
    }
}

const createPost = (url, post, groupID) => {
    return (dispatch) => {
        request
            .post(url)
            .set('X-CSRFToken', window.django.csrf)
            .send({'post': post, 'groupID': groupID})
            .end((err, res) => {
                if (res.ok) {
                    dispatch(addSinglePost(res.body))
                }
            })
    }
}

const updatePost = (url, post) => {
    return (dispatch) => {
        request
            .put(url)
            .set('X-CSRFToken', window.django.csrf)
            .send({ 'post': post })
            .end((err, res) => {
                if (res.ok) {
                    dispatch(updateSinglePost(res.body))
                }
            })
    }
}

const deletePost = (url, postID) => {
    return (dispatch) => {
        request
            .delete(url)
            .set('X-CSRFToken', window.django.csrf)
            .end((err, res) => {
                if (res.status === 204) {
                    dispatch(deleteSinglePost(postID))
                }
            })
    }
}

const approvePost = (url) => {
    return (dispatch) => {
        request
            .patch(url)
            .set('X-CSRFToken', window.django.csrf)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(updateSinglePost(res.body))
                }
            })
    }
}

const getComments = (url) => {
    return (dispatch) => {
        request
            .get(url)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(commentLoadSuccess(res.body))
                }
            })
    }
}

const createComment = (url, comment, postID) => {
    return (dispatch) => {
        request
            .post(url)
            .set('X-CSRFToken', window.django.csrf)
            .send({'comment': comment, 'postID': postID})
            .end((err, res) => {
                if (res.ok) {
                    dispatch(addSingleComment(res.body))
                    dispatch(updateCommentCount(postID))
                }
            })
    }
}

const deleteComment = (url, commentID, postID) => {
    return (dispatch) => {
        request
            .delete(url)
            .set('X-CSRFToken', window.django.csrf)
            .end((err, res) => {
                if (res.status === 204) {
                    dispatch(deleteSingleComment(commentID))
                    dispatch(updateCommentCount(postID, true))
                }
            })
    }
}

const approveComment = (url) => {
    return (dispatch) => {
        request
            .patch(url)
            .set('X-CSRFToken', window.django.csrf)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(updateSingleComment(res.body))
                }
            })
    }
}

export const actions = {
    createPost,
    getPosts,
    deletePost,
    approvePost,
    getComments,
    deleteComment,
    createComment,
    approveComment,
    updateEditingPost,
    updatePost
}


export default function GroupPostReducer(state=INITIAL_STATE, action) {
    switch(action.type) {
    case POSTS_ARE_LOADING:
        return {
            ...state, isLoading: action.status
        }
    case POST_LOAD_SUCCESS:
        return {
            ...state, posts: action.posts
        }
    case ADD_SINGLE_POST:
        return {
            ...state, posts: [...state.posts, action.post]
        }
    case DELETE_SINGLE_POST:
        return {
            ...state, posts: state.posts.filter(x => x.id !== action.postID)
        }
    case UPDATE_SINGLE_POST:
        return {
            ...state, posts: state.posts.map(
                x => x.id === action.post.id ? action.post : x
            )
        }
    case COMMENT_LOAD_SUCCESS:
        return {
            ...state, comments: action.comments
        }
    case ADD_SINGLE_COMMENT:
        return {
            ...state, comments: [...state.comments, action.comment]
        }
    case DELETE_SINGLE_COMMENT:
        return {
            ...state, comments: state.comments.filter(x => x.id !== action.commentID)
        }
    case UPDATE_SINGLE_COMMENT:
        return {
            ...state, comments: state.comments.map(
                x => x.id === action.comment.id ? action.comment : x
            )
        }
    case UPDATE_COMMENT_COUNT:
        return {
            ...state, posts: state.posts.map(
                x => x.id === action.postID ?
                    action.negative ?
                        { ...x, comment_count: x.comment_count - 1 } :
                        { ...x, comment_count: x.comment_count + 1 } :
                    x
            )
        }
    case UPDATE_EDITING_POST:
        return {...state, editingPost: action.postID}
    default:
        return state
    }
}
