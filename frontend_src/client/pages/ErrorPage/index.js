import React from 'react'
import classnames from 'classnames'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './ErrorPage.styl'


class ErrorPage extends React.Component {
    render() {
        const {
            code,
            message
        } = this.props.route
        const cx = classnames(s.container)

        return (
            <div className={cx}>
                <p className='error-code'>{code}</p>
                <p className='error-message'>Can't find the page you're looking for</p>
            </div>
        )
    }
}

export default withStyles(s)(ErrorPage)
