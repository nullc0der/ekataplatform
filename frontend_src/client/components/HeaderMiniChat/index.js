import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './HeaderMiniChat.styl'

import Dropdown from 'components/ui/Dropdown'
import {actions as chatActions} from 'store/Chat'


import Avatar from 'components/Avatar'

import RECENT_CHATS from 'pages/Messenger/sample-chats'

class HeaderMiniChat extends Component {
    static contextTypes = {
        router: PropTypes.object
    }

    openMiniChat = (chat)=> (e)=> {
        if ( $(window).width() > 768 )
            this.props.openMiniChat(chat)
        else
            this.context.router.push('/messenger/'+chat.id)
    }

    renderItem = (item, i)=> {
        return (
            <div
                onClick={this.openMiniChat(item)}
                className={`flex-horizontal ${c.item}`}>
                <Avatar
                    name={item.username}/>
                <div className='item-details'>
                    <div className='item-name'>
                        {item.username}
                    </div>
                    <div className='item-desc'>
                        {item.description}
                    </div>
                </div>
            </div>
        )
    }

    render(){
        const {
            className,
            username = 'sharad_kant'
        } = this.props

        const cx = classnames(c.container, className)

        const labelClass = classnames('flex-horizontal', 'a-center', c.label)

        const labelImageStyle = {
            // backgroundImage: `url('https://placehold.it/48x48')`
        }

        const label = (
            <span className={labelClass}>
                <i className='fa fa-fw fa-comment-o'/>
            </span>
        )


        return (
            <Dropdown
                id='id-header-mini-chat'
                className={cx}
                label={label}
                ref={dd => this.dropdown = dd}
                items={RECENT_CHATS}
                itemRenderer={this.renderItem}/>
        )
    }
}
const mapStateToProps = (state)=> ({

})

const mapDispatchToProps = (dispatch)=> ({
    openMiniChat(chat){
        return dispatch(chatActions.openMiniChat(chat))
    }
})

export default withStyles(c)(
    connect(mapStateToProps,mapDispatchToProps)(HeaderMiniChat)
)
