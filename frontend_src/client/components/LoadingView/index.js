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

    const imageURL = window.django.site_type.trim() !== 'local' ? "/statics/dist/img/Preloader_2.gif" : "/static/dist/img/Preloader_2.gif"

    return (
      <div className={cx}>
        <img src={imageURL}/>
      </div>
    )
  }
}

export default withStyles(c)(LoadingView)
