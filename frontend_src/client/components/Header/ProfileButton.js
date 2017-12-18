import {Component} from 'react'
import classnames  from 'classnames'

import Dropdown from 'components/ui/Dropdown'
import Avatar from 'components/Avatar'

const USER = [{
    image: window.django.user.profile_image,
    username: window.django.user.username,
    fullname: window.django.user.fullname,
    profile_avatar_color: window.django.user.profile_avatar_color,
    created_at_text: `Member since: ${window.django.user.date_joined}` ,
}]

export default class HeaderProfileButton extends Component {
    state = {
        isOpen: false
    }

    toggleOpen = ()=> {
        this.setState({isOpen: !this.state.isOpen})
    }

    componentDidMount = ()=> {
      // $(document).on('blur' , '.header-profile-button', this.onBlur)
    }
    componentWillUnmount = ()=> {
      // $(document).off('blur', '.header-profile-button', this.onBlur)
    }

    onBlur = (e)=> {
        console.log('blurred')
    }

    renderProfile = (user)=> {
        return <div className='profile-menu'>
            <div className='flex-vertical a-center j-center blue-container'>
                <div className='profile-icon big rounded no-overflow'>
                    {
                        user.image ?
                        <img className='img-responsive rounded' src={user.image}/> :
                        <Avatar name={user.fullname ? user.fullname : user.username} bgcolor={user.profile_avatar_color} fontsize="3em"/>
                    }
                </div>
                <div className='text-center'> {user.created_at_text} </div>
            </div>
            <div className='flex-horizontal user-menu j-between'>
                <a className='profile-link' href='/profile/#reference'>
                    References
                </a>
                <a className='profile-link' href='/myaccount/'>
                    Account
                </a>
                <a className='profile-link' href='/'>
                    Landing
                </a>
            </div>
            <div className='profile-menu-footer flex-horizontal j-between'>
                <a className='btn footer-btn' href='/profile/'> Profile </a>
                <a className='btn footer-btn' href='/logout/'> Sign Out </a>
            </div>
        </div>
    }

    render(){
        const {
            className,
            user = USER
        } = this.props;

        const cx = classnames('header-profile-button', className)
        const menuClass = classnames('profile-menu', {
            'is-open': this.state.isOpen
        })

        const label = (
            <div
                className='profile-button flex-horizontal a-center'>
                <div className='profile-icon rounded no-overflow'>
                    {
                        user[0].image ?
                        <img className='img-responsive rounded' src={user[0].image}/> :
                        <Avatar name={user[0].fullname ? user[0].fullname : user[0].username} bgcolor={user[0].profile_avatar_color} fontsize="0.5em"/>
                    }
                </div>
                <div className='profile-username'> {user[0].username} </div>
            </div>
        )



        return (
            <Dropdown
                id='id-header-profile-dropdown'
                className={cx}
                label={label}
                items={USER}
                itemRenderer={this.renderProfile}/>
        )
    }
}
