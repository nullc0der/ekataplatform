import { actions as commonActions } from './Common'
import request from 'superagent'


const INITIAL_STATE = {
    group: {
        'id': 0,
        'group_url': '',
        'name': '',
        'description': '',
        'ldescription': '',
        'group_type': '',
        'header_image_url': '',
        'logo_url': '',
        'members': [],
        'subscribers': [],
    }
}

const LOAD_GROUP_SUCCESS = 'LOAD_GROUP_SUCCESS'
const loadGroupSuccess = (group) => ({
    type: LOAD_GROUP_SUCCESS,
    group
})

const loadGroup = (url) => {
    return (dispatch) => {
        request
            .get(url)
            .end((err, res) => {
                if (res.ok) {
                    dispatch(loadGroupSuccess(res.body))
                }
            })
    }
}

const editGroup = (url, payload, logo=null, header=null) => {
    return (dispatch) => {
        const req = request
            .post(url)
            .set('X-CSRFToken', window.django.csrf)
        if (logo) {
            req.attach('logo', logo)
        }
        if (header) {
            req.attach('header_image', header)
        }
        req.field(payload)
        req.end((err, res) => {
            if (res.ok) {
                dispatch(loadGroupSuccess(res.body))
            }
            if(err && err.status === 400) {
                for (const e of res.body) {
                    dispatch(commonActions.addNotification({
                        level: 'error',
                        message: e
                    }))   
                }
            }
        })
    }
}

export const actions = {
    loadGroup,
    editGroup
}

export default function GroupSettingsReducer(state=INITIAL_STATE, action) {
    switch(action.type) {
        case LOAD_GROUP_SUCCESS:
            return {
                ...state, group: action.group
            }
        default:
            return state
    }
}
