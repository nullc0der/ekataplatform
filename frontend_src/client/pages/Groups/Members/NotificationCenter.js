import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import Avatar from 'components/Avatar'

import c from './Members.styl'

class NotificationCenter extends Component {
	state = {
		list: [
			{name: 'John Doe', subtext: 'was added by Admin'},
			{name: 'Wohn Poe', subtext: 'sent a request to join'},
			{name: 'Kohn Moe', subtext: 'was added by Admin'},
			{
				name: 'Fohn Doe',
				subtext: 'was blocked by Admin',
				prompt: {
					'yes': '/requests/randomid1234/accept',
					'no': '/requests/randomid1234/deny'
				}
			},
			{name: 'Bohn Poe', subtext: 'posted recently'},
			{name: 'Wohn Hoe', subtext: 'was added by Admin'},
			{
				name: 'Cohn Toe',
				subtext: 'sent a request to join',
				prompt: {
					'yes': '/requests/randomid1234/accept',
					'no': '/requests/randomid1234/deny'
				}
			},
			{name: 'Fohn Joe', subtext: 'was added by Admin'},
			{name: 'Mohn Loe', subtext: 'was blocked by Admin'},
			{name: 'Rohn Poe', subtext: 'posted recently'},
		]
	}
	render(){
		const {
			className
		} = this.props;

		const {
			list
		} = this.state;

		const cx = classnames(className, 'flex-vertical')

		return (
			<div className={cx}>
				<div className='nc-header'>
					Notification Center
				</div>
				<div className='nc-list flex-1 scroll-y'>
					{
						list.map((x, i)=> {
							return <div key={i} className='nc-list-item flex-horizontal a-center'>
								<Avatar
									name={x.name}/>
								<div className='details'>
									<div className='name'> {x.name} </div>
									<div className='subtext'> {x.subtext} </div>
								</div>
								<div className='flex-1'/>
								{
									x.prompt && x.prompt.yes && <div className='nf-btn btn-accept' data-action={x.prompt.yes}>
										Accept
									</div>
								}
								{
									x.prompt && x.prompt.no && <div className='nf-btn btn-deny' data-action={x.prompt.no}>
										Deny
									</div>
								}
							</div>
						})
					}
				</div>
			</div>
		)
	}
}

export default NotificationCenter
