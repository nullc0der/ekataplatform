import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

var counter = 0;

export default function DOMComponent(ChildComponent){
    class DOMComponent extends Component {

        constructor(...args){
            super(...args)
            this._domCompID = '-dom-comp-'+(++counter)

            window.xx = this
        }

        _bindElements = ()=> {
            if (typeof ChildComponent.ui !== 'object')
                return

            Object.keys(ChildComponent.ui).forEach(keyname=>{
                if (typeof keyname !== 'string')
                    return

                let _classname = `.${this._domCompID} .${ChildComponent.ui[keyname]}`
                console.log('finding classname: ', _classname)
                ChildComponent.ui[keyname] = $( _classname )
            })

            this.ui = ChildComponent.ui
        }

        componentDidMount = ()=> {
            this._bindElements()
        }

        render(){
            const {
                className,
                ...others
            } = this.props;
            const cx = classnames(this._domCompID, className )
            return <ChildComponent className={cx} {...others}/>
        }

    }

    return DOMComponent
}
