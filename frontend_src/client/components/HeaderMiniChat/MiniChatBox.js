import React from 'react'
import classnames from 'classnames'
import _ from 'lodash'

import ChatBodyItem from 'components/ChatBodyItem'
import ChatFooter from 'components/ChatFooter'

export default class MiniChatBox extends React.Component {

    componentDidMount = () => {
        if (this.props.chat) {
            let unreadIds = this.props.chat.messages.filter(x => !x.read & x.user.username !== window.django.user.username)
            if (unreadIds) {
                this.props.handleUnreadChat(this.props.chat.roomId, unreadIds)
            }
            this.scrollToBottom()
        }
    }

    componentDidUpdate = (prevProps) => {
        if (prevProps.chat !== this.props.chat) {
            let unreadIds = this.props.chat.messages.filter(x => !x.read & x.user.username !== window.django.user.username)
            if (unreadIds) {
                this.props.handleUnreadChat(this.props.chat.roomId, unreadIds)
            }
            this.scrollToBottom()
        }
    }

    scrollToBottom = () => {
        this.scrollEl.scrollIntoView()
    }

    render() {
        const { chat, selectedMessages, uploadProgress, onlineUsers } = this.props
        const cx = classnames('chat-header', 'flex-horizontal', 'a-center', 'j-between', { 'is-online': _.includes(onlineUsers, chat.username) })
        return <div className='mini-chat flex-vertical'>
            <div className={cx}>
                <div className='username'> {chat.username} </div>
                <div className='chat-options'>
                    {
                        selectedMessages[chat.roomId] && selectedMessages[chat.roomId].length > 0 &&
                        <div
                            onClick={() => this.props.handleDeleteChat(chat.roomId)}
                            className='btn btn-default ui-button'>
                            <i className='fa fa-trash' />
                        </div>
                    }
                    <div
                        onClick={this.props.toggleMinimise}
                        className='btn btn-default ui-button'>
                        <i className='fa fa-window-minimize' />
                    </div>
                    <div
                        onClick={this.props.closeChat(chat.roomId)}
                        className='btn btn-default ui-button'>
                        <i className='fa fa-remove' />
                    </div>
                </div>
            </div>
            <div className='chat-body flex-1'>
                {
                    chat.messages.map((x, i) => {
                        return <ChatBodyItem
                            key={i}
                            roomId={chat.roomId}
                            user={x.user}
                            message={x.message}
                            fileurl={x.fileurl}
                            filetype={x.filetype}
                            filename={x.filename}
                            message_id={x.id}
                            stamp={new Date(x.timestamp)}
                            left={x.user.username !== window.django.user.username}
                            selected={_.includes(selectedMessages[chat.roomId], x.id)}
                            onSelected={this.props.handleSelectedMessage}
                            miniChat={true} />
                    })
                }
                <div style={{ float: "left", clear: "both" }} ref={el => this.scrollEl = el}></div>
            </div>
            <ChatFooter
                small={true}
                roomId={chat.roomId}
                handleSendChat={this.props.handleSendChat}
                handleTypingStatus={this.props.handleTypingStatus}
                showTyping={chat.roomId === this.props.websocketTypingStatus}
                showTypingUsername={chat.username}
                uploadProgress={uploadProgress.roomId === chat.roomId ? uploadProgress.progress : 0} />
        </div>
    }
}
