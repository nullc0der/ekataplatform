import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './HeaderMiniChat.styl'

import Dropdown from 'components/ui/Dropdown'
import {actions as chatActions} from 'store/Chat'
import { roomsFetchData } from 'store/Chatrooms'
import { actions as commonActions } from 'store/Common'


import Avatar from 'components/Avatar'

class HeaderMiniChat extends Component {
    static contextTypes = {
        router: PropTypes.object
    }

    componentDidMount = () => {
        if(!this.context.router.location.pathname.startsWith('messenger/')) {
            this.props.fetchData('/api/messaging/chatrooms/')
        }
    }

    openMiniChat = (roomId)=> (e)=> {
        if ( $(window).width() > 768 ){
            this.props.openMiniChat(roomId)
        }
        else {
            this.context.router.push('/messenger/' + roomId)
            this.props.updateHeaderVisibility(false)
        }
    }

    renderItem = (item, i)=> {
        return (
            <div
                onClick={this.openMiniChat(item.id)}
                className={`flex-horizontal ${c.item}`}>
                <div className='item-image rounded'>
                    {
                        item.user_image_url ?
                            <img className='img-responsive rounded' src={item.user_image_url} /> :
                            <Avatar name={item.username} bgcolor={item.user_avatar_color} fontsize="2em" />
                    }
                </div>
                <div className='item-details'>
                    <div className='item-name'>
                        {item.username}
                    </div>
                    <div className='item-desc'>
                        {item.unread_count} unread
                    </div>
                </div>
            </div>
        )
    }

    render(){
        const {
            className
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
                items={this.props.rooms}
                itemRenderer={this.renderItem}/>
        )
    }
}
const mapStateToProps = (state)=> ({
    rooms: state.ChatRooms.rooms
})

const mapDispatchToProps = (dispatch)=> ({
    openMiniChat: (roomId) => dispatch(chatActions.openMiniChat(roomId)),
    fetchData: (url) => dispatch(roomsFetchData(url)),
    updateHeaderVisibility: (showHeaders) => dispatch(commonActions.updateHeaderVisibility(showHeaders))
})

export default withStyles(c)(
    connect(mapStateToProps,mapDispatchToProps)(HeaderMiniChat)
)
