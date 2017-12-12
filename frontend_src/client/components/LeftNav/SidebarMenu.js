import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import Link from 'react-router/lib/Link'
import withRouter from 'react-router/lib/withRouter'

import MENU_ITEMS from './menu-items'

const debug = require('debug')('ekata:sidebar-menu')

class SidebarMenu extends Component {
	state = {
		selectedItemIndex: 0
	}

	componentDidMount = ()=>  {
		$(document).on('click', '.is-clickable', this.setBreadCrumbs)
	}

	componentWillUnmount = ()=> {
		$(document).off('click', '.is-clickable', this.setBreadCrumbs)
	}

	selectPrimaryItem = (item, index)=> {
		debug('Selected Item: ', item, index)
		this.setState({selectedItemIndex: index})
	}

	setBreadCrumbs = (e)=> {
		var $el = $(e.currentTarget)
	}

	toggleSubMenu = (e)=> {
		e.preventDefault();
		e.stopPropagation();
		var $el = $(e.currentTarget)
		var $dd = $el.find('.menu-dropdown')

		$('.secondary-menu-item .menu-dropdown').each(function(){
			if ( $(this).is($dd) ){
				$(this).toggleClass('is-open', !$(this).hasClass('is-open'))
			} else {
				$(this).removeClass('is-open')
			}
		})
	}

	navigate = (e)=> {
		e.stopPropagation();
		e.preventDefault();
		let $el = $(e.currentTarget)
		let url = $el.attr('data-href')

		if (!url){
			$el = $el.parents('.is-clickable')
			url = $el.attr('data-href')
		}

		debug('Navigating to: ', url)

		if (!url)
			return
		this.props.router.push(url)
	}


	withActiveClass = (href='#', prefixClass = '')=> {
		var path = this.props.location.pathname || '';

		path = path.trim()
		href = href.trim()

		return path.indexOf(href)!== -1
			? `${prefixClass} is-active`
			: prefixClass
	}

	render(){
		const {
			className
		} = this.props;

		const cx = classnames(className, 'flex-horizontal')

		const subMenuItems = MENU_ITEMS[this.state.selectedItemIndex].children

		return (
			<div className={cx}>
				<div className='primary-menu'>
					{
						MENU_ITEMS.map((x, i)=> {
							const cx = classnames(
								'primary-menu-item', 'no-outline', 'is-clickable', {
									'is-active': i === this.state.selectedItemIndex
								}
							)

							return <Link
								key={i}
								to={x.href}
								onClick={()=> this.selectPrimaryItem(x, i)}
								className={cx}>
								<i className={x.icon}></i>
							</Link>
						})
					}
				</div>
				<div className='secondary-menu'>
					{
						subMenuItems.map((x, i)=> (
							<div
								key={i}
								data-href={x.href}
								onClick={x.href ? this.navigate : this.toggleSubMenu}
								className={
									this.withActiveClass(x.href, 'secondary-menu-item no-outline is-clickable')
								}>
								<div className='menu-inner'>
									<span className='menu-icon'>
										<i className={x.icon}/>
									</span>
									<span className='menu-name flex-horizontal a-center'>
										<span className='flex-1'> {x.name} </span>
										{
											!!x.children && <div
												className='menu-dropdown-toggle'>
												<i className='fa fa-fw fa-chevron-down'/>
											</div>
										}
									</span>
								</div>
								{
									!!x.children && <div className='menu-dropdown'>
										{
											x.children.map((child, childIndex)=> (
												<div
													key={childIndex}
													data-href={child.href}
													onClick={this.navigate}
													className={this.withActiveClass(child.href, 'sub-submenu-item is-clickable')}>
													<span className='sub-submenu-icon'>
														<i className={child.icon}/>
													</span>
													<span className='sub-submenu-name'>
														{child.name}
													</span>
												</div>
											))
										}
									</div>
								}
							</div>
						))
					}
				</div>
			</div>
		)
	}
}

export default withRouter(SidebarMenu)
