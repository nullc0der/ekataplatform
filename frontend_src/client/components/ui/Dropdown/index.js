import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles from 'isomorphic-style-loader/lib/withStyles'
import c from './Dropdown.styl'


class UIDropdown extends Component {

    static propTypes = {
        items: PropTypes.array.isRequired,
        itemRenderer: PropTypes.func.isRequired,
        id: PropTypes.string.isRequired
    }

    state = {
        isOpen: false
    }

    componentWillReceiveProps = (nextProps)=> {
        this.setState({isOpen: nextProps.isOpen})
    }

    componentDidMount = ()=> {
        window.xx = this
        if (typeof this.props.ref === "function"){
            this.props.ref(this)
        }
        // $(document).on('click', `.${c.toggle}`, this.toggleOpen)
        // $(document).on('blur' , `.${c.container}`, this.onBlur)
        $(this.root).find('.ui-dropdown-item').on('click', this.closeDD)
    }

    componentWillUnmount = ()=> {
        // $(document).off('click', `.${c.toggle}`, this.toggleOpen)
        // $(document).off('blur' , `.${c.container}`, this.onBlur)
        $(this.root).find('.ui-dropdown-item').off('click', this.closeDD)
    }

    toggleOpen = ()=> {
        this.setState({isOpen: !this.state.isOpen})
    }

    closeDD = ()=> {
        $(this.root)
            .find('.ui-dropdown-list.is-active, .ui-dropdown-toggle.is-active')
            .removeClass('is-active')
    }

    handleClick = (e)=> {
        let $root   = $(this.root)
        let $toggle = $(e.currentTarget)

        $root.parent().find('.ui-dropdown').each(function(){
            if ($(this).is($root)){
                $(this).find('.ui-dropdown-toggle').hasClass('is-active')
                    ? $(this).find('.ui-dropdown-toggle, .ui-dropdown-list').removeClass('is-active')
                    : $(this).find('.ui-dropdown-toggle, .ui-dropdown-list').addClass('is-active')
            } else {
                $(this).find('.ui-dropdown-toggle, .ui-dropdown-list').removeClass('is-active')
            }
        })
    }

    render(){
        const {
            className,
            label = 'Dropdown',
            listItemClass = '',
            items = [],
            itemRenderer,
            dropdownFooter= false
        } = this.props

        const cx = classnames(c.container, className, 'ui-dropdown', {
            'has-footer': !!dropdownFooter
        })

        const toggleClass = classnames(c.toggle, 'ui-dropdown-toggle', {
            'is-active': this.state.isOpen
        })

        const listClass = classnames(c.list, 'flex-vertical', 'ui-dropdown-list', {
            'is-active': this.state.isOpen
        })

        const itemClass = classnames(c.listItem, 'ui-dropdown-item', listItemClass)

        const footerClass = classnames(c.footer, 'ui-dropdown-footer', {
            'is-hidden': !dropdownFooter
        })

        return (
            <div
                className={cx}
                ref={node => this.root = node}>
                <div
                    onClick={this.handleClick}
                    className={toggleClass}>
                    {label}
                </div>
                <div className={listClass}>
                    <div className='list-inner'>
                        {
                            items.map((x, i)=> (
                                <div key={i} className={itemClass}>
                                    {itemRenderer(x,i)}
                                </div>
                            ))
                        }
                    </div>
                    <div className={footerClass}>
                        {dropdownFooter}
                    </div>
                </div>
            </div>
        )
    }
}

export default withStyles(c)(UIDropdown)
