import {Component} from 'react'
import classnames  from 'classnames'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './Profile.styl'

class DashboardProfilePage extends Component {
    render(){
        const {className} = this.props;
        const cx = classname(className)
        return (
            <div className={cx}>
                Dashboard Profile Page
            </div>
        )
    }
}


export default withStyles(c)(DashboardProfilePage)
