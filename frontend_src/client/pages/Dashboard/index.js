import {Component} from 'react'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './Dashboard.styl'

class DashboardPage extends Component {
    render(){
        const cx = classnames(c.container)
        return (
            <div className={cx}>
                Dashboard Page
            </div>
        )
    }
}

export default withStyles(c)(DashboardPage)
