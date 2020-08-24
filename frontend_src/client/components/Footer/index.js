import {Component} from 'react'
import PropTypes   from 'prop-types'

import classnames  from 'classnames'


import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './Footer.styl'

class Footer extends Component {
    render(){
        const {className} = this.props;
        const cx = classnames(c.container, className, 'ui-footer flex-horizontal', 'a-stretch')
        return (
            <div className={cx}>
                <div className='flex-horizontal a-center'>
                    <b>
                        Copyright &copy; 2014-2016 Ekata.&nbsp;
                    </b>
                    <span>
                        All rights reserved.
                    </span>
                    <span className='pill pill-blue pill-powered'> Powered by Ekata </span>
                </div>
                <div className='flex-1'/>
                <div className='flex-horizontal a-center'>
                    <div className='pill pill-red pill-beta'> beta </div>
                    <b> v0.7.5 </b>
                </div>

            </div>
        )
    }
}

export default withStyles(c)(Footer)
