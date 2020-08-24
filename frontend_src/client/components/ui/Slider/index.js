import React from 'react'
import classnames from 'classnames'

import s from './Slider.styl'
import withStyles from 'isomorphic-style-loader/lib/withStyles'


class Slider extends React.Component {
    render() {
        const {
            name,
            value,
            min,
            max,
            onChange,
            className,
            step="1"
        } = this.props

        const cx = classnames(s.container, className)

        return (
            <div className={cx}>
                <input type="range" name={name} min={min} max={max} value={value} onChange={onChange} step={step}/>
            </div>
        )
    }
}

export default withStyles(s)(Slider)
