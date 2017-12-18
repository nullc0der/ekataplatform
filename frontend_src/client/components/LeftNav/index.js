import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import Avatar from 'components/Avatar'
import c from './LeftNav.styl'

import SidebarMenu from './SidebarMenu'

import {actions as commonActions} from 'store/Common'

class LeftNav extends Component {

	toggleIfThin = ()=> {
		var w = $(window).width();
		if (!this.props.open || w < 769)
			return
		console.log('should toggle the nav')
		this.props.onRequestToggle();
	}

	render(){
		const {
			className,
			open = false
		} = this.props;

		const cx = classnames(
			c.container, className,
			'flex-vertical',
			{ 'is-open': open}
		)

		return (
			<div className={cx}>
				<div
					className='leftnav-backdrop'
					onClick={this.props.onRequestToggle}/>
				<div className='sidebar-header flex-horizontal a-center j-center'>
					EKATA
				</div>
				<div className='sidebar-sub-header'>
					<div className='user-block flex-horizontal'>
						<div className='user-image'>
							{
                        		window.django.user.profile_image ?
                        		<img className='img-responsive rounded' src={window.django.user.profile_image}/> :
                        		<Avatar name={window.django.user.fullname ? window.django.user.fullname : window.django.user.username} bgcolor={window.django.user.profile_avatar_color} fontsize="2em"/>
                    		}
						</div>
						<div className='user-details flex-1'>
							<div className='name'> { window.django.user.username } </div>
							<div className='status is-online'> Online </div>
						</div>
					</div>
					<div
						className='menu-search'
						onClick={this.toggleIfThin}>
						<input className='search-input no-outline' placeholder='Search...'/>
						<span className='search-icon'>
							<i className='material-icons'>search</i>
						</span>
					</div>
				</div>
				<SidebarMenu
					className='sidebar-menu'/>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	breadcrumbs: state.Common.breadcrumbs
})

const mapDispatchToProps = (dispatch)=> ({
	setBreadCrumbs(b){
		return dispatch(commonActions.setBreadCrumbs(b))
	}
})

export default withStyles(c)(
	connect(mapStateToProps, mapDispatchToProps)(LeftNav)
)
