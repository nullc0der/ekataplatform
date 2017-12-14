import React from 'react'
import request from 'superagent'

const debug = require('debug')('ekata:onlinesetter')

export default class OnlineSetter extends React.Component {
    componentDidMount() {
        this.onlineSetter = setInterval(
            () => this.setOnline(),
            15000
        )
    }

    componentWillUnmount() {
        clearInterval(this.onlineSetter)
    }

    setOnline() {
        request
            .post(window.django.setonline_url)
            .set('X-CSRFToken', window.django.csrf)
            .end((err, res) => {
                if (err || !res.ok ) {
                    debug("Setting online failed")
                } else {
                    debug("Online status posted")
                }
            })
    }

    render() {
        return null
    }
}
