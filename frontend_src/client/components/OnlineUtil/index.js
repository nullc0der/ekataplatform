import React from 'react'
import request from 'superagent'
import { connect } from 'react-redux'

import { fetchOnlineUsers } from 'store/Users'

class OnlineUtil extends React.Component {
    componentDidMount() {
        this.setOnline()
        this.onlineSetter = setInterval(
            () => this.setOnline(),
            15000
        )
        this.props.fetchOnlineUsersList('/onlineusers/')
        this.onlineGetter = setInterval(
            () => this.props.fetchOnlineUsersList('/onlineusers/'),
            20000
        )
    }

    componentWillUnmount() {
        clearInterval(this.onlineSetter)
        clearInterval(this.onlineGetter)
    }

    setOnline() {
        request
            .post(window.django.setonline_url)
            .set('X-CSRFToken', window.django.csrf)
            .end()
    }

    render() {
        return null
    }
}

const mapStateToProps = (state) => ({

})


const mapDispatchToProps = (dispatch) => ({
    fetchOnlineUsersList: (url) => dispatch(fetchOnlineUsers(url))
})

export default connect(mapStateToProps, mapDispatchToProps)(OnlineUtil)
