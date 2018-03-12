import request from 'superagent'


const INITIAL_STATE = {
    posts: [],
    isLoading: false
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

const UPDATE_SINGLE_POST = 'UPDATE_SINGLE_POST'
const updateSinglePost = (post) => ({
    type: UPDATE_SINGLE_POST,
    post
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
                    dispatch(updateSinglePost(res.body))
                }
            })
    }
}

export const actions = {
    createPost,
    getPosts
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
        case UPDATE_SINGLE_POST:
            return {
                ...state, posts: [...state.posts, action.post]
            }
        default:
            return state
    }
}
