import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import c from './Members.styl'

class Advertisement extends Component {
	state = {
		selected: 0,
		items: [
			{title: 'Ad for company 1', image: 'https://unsplash.it/512/?image=0'},
			{title: 'Ad for company 2', image: 'https://unsplash.it/512/?image=1'},
			{title: 'Ad for company 3', image: 'https://unsplash.it/512/?image=2'},
			{title: 'Ad for company 4', image: 'https://unsplash.it/512/?image=3'},
			{title: 'Ad for company 5', image: 'https://unsplash.it/512/?image=4'},
		]
	}

	goNext = ()=> {
		var current = this.state.selected
		var next = 0
		if (current + 1 < this.state.items.length){
			next = current + 1
		}
		this.setState({
			selected: next
		})
	}
	goPrev = ()=> {
		var current = this.state.selected
		var prev = this.state.items.length-1
		if (current - 1 >= 0){
			prev = current - 1
		}
		this.setState({
			selected: prev
		})
	}

	render(){
		const {
			className
		} = this.props;

		const {
			selected,
			items
		} = this.state;

		const item = items[selected] || {}

		const cx = classnames(className, 'flex-vertical')

		return (
			<div className={cx}>
				<div className='flex-1 ad-image' style={{
					backgroundImage: `url('${item.image}')`
				}}>
				</div>
				<div className='ad-controls flex-horizontal a-center'>
					<div
						onClick={this.goPrev}
						className='ad-control control-left'>
						<i className='fa fa-fw fa-chevron-left'/>
					</div>
					<div className='ad-title flex-1'>
						{item.title}
					</div>
					<div
						onClick={this.goNext}
						className='ad-control control-right'>
						<i className='fa fa-fw fa-chevron-right'/>
					</div>
				</div>
			</div>
		)
	}
}

export default Advertisement
