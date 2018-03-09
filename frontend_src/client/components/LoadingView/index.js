import React from 'react'
import classnames from 'classnames'

import c from './LoadingView.styl'
import withStyles from 'isomorphic-style-loader/lib/withStyles'

class LoadingView extends React.Component {
  render() {
    const {
      className
    } = this.props
    const cx = classnames(c.container, className)

    return (
      <div className={cx}>
        <img src="/static/dist/img/Preloader_2.gif"/>
      </div>
    )
  }
}

export default withStyles(c)(LoadingView)
