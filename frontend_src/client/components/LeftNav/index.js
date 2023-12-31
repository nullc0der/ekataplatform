import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'
import {connect}   from 'react-redux'
import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import Avatar from 'components/Avatar'
import SiteLabel from 'components/SiteLabel'
import c from './LeftNav.styl'

import SidebarMenu from './SidebarMenu'

import {actions as commonActions} from 'store/Common'

class LeftNav extends Component {

	componentDidMount = () => {
		if (this.props.lastGroup) {
			const url = `/api/groups/${this.props.lastGroup}/roles/`
			this.props.fetchPermissions(url, this.props.lastGroup)
		}
	}

	componentDidUpdate = (prevProps) => {
		if (prevProps.lastGroup !== this.props.lastGroup && this.props.lastGroup) {
			const url = `/api/groups/${this.props.lastGroup}/roles/`
			this.props.fetchPermissions(url, this.props.lastGroup)
		}
	}

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
			menuItems,
			groupMenus,
			open = false
		} = this.props;

		const cx = classnames(
			c.container, className,
			'flex-vertical',
			{ 'is-open': open}
		)

		return (
			<div className={cx}>
				{ window.django.site_type.trim() === 'beta' && <SiteLabel isVisible={true}/> }
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
					className='sidebar-menu'
					menuItems={[...menuItems, groupMenus]}/>
			</div>
		)
	}
}

const mapStateToProps = (state)=> ({
	breadcrumbs: state.Common.breadcrumbs,
	menuItems: state.Common.menuItems,
	groupMenus: state.Common.groupMenus,
	lastGroup: state.Groups.lastGroup
})

const mapDispatchToProps = (dispatch)=> ({
	setBreadCrumbs(b){
		return dispatch(commonActions.setBreadCrumbs(b))
	},
	fetchPermissions: (url, groupID) => {
		dispatch(commonActions.fetchPermissions(url, groupID))
	}
})

export default withStyles(c)(
	connect(mapStateToProps, mapDispatchToProps)(LeftNav)
)
