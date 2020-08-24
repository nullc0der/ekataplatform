import React from 'react'
import classnames from 'classnames'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './SiteLabel.styl'


class SiteLabel extends React.Component {
    render() {
        const {
            className,
            isVisible=false,
            label='beta'
        } = this.props
  
        const cx = classnames(s.container, className, {
            'is-visible': isVisible
        })

        return (
            <div className={cx}>
                <div className="ribbon"><span>{label}</span></div>
            </div>
        )
    }
}

export default withStyles(s)(SiteLabel)
