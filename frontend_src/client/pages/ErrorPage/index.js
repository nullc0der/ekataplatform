import React from 'react'
import classnames from 'classnames'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './ErrorPage.styl'


const messages = {
    '404': "Couldn't find the page you're looking for",
    '403': "Sorry you don't have permission to access this page"
}


class ErrorPage extends React.Component {
    render() {
        const {
            code
        } = this.props.route
        const cx = classnames(s.container)

        return (
            <div className={cx}>
                <div className='error-code'><p>{code}</p></div>
                <div className='error-message'>
                    <p>{messages[code]}</p>
                    <a className="btn btn-home" href='/'>Take me to home</a>
                </div>
            </div>
        )
    }
}

export default withStyles(s)(ErrorPage)
