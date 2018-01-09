import {Component} from 'react'
import PropTypes   from 'prop-types'
import classnames  from 'classnames'

import withStyles  from 'isomorphic-style-loader/lib/withStyles'
import c from './Modal.styl'

class UIModal extends Component {
	state = {
		isOpen: false
	};

	static propTypes = {
		id: PropTypes.string.isRequired,
		isOpen: PropTypes.bool.isRequired
	}

	componentDidMount = ()=> {
		if ( this.props.isOpen !== this.state.isOpen )
			this.setState({isOpen: this.props.isOpen})
	}

	componentWillReceiveProps = (nextProps)=> {
		if (nextProps.isOpen !== this.props.isOpen)
			this.setState({ isOpen: nextProps.isOpen })
	}

	render(){
		const {
			className,
			id,
			title = 'Modal Title',
			footer = false,
			detachedFooter = false,
			detachedFooterText = 'Submit',
			children
		} = this.props;

		const cx = classnames(c.container, 'ui-modal flex-vertical a-center j-center', className, {
			'is-open': this.state.isOpen
		})

		const backdropClass = classnames(c.backdrop, 'ui-modal-backdrop')
		const contentClass  = classnames(c.content,  'flex-vertical ui-modal-content')

		const headerClass   = classnames(c.header, 'flex-horizontal a-center ui-modal-header', {
			hidden: !title
		})
		const bodyClass     = classnames(c.body, 'flex-1 scroll-y ui-modal-body')

		const footerClass   = classnames(c.footer, 'ui-modal-footer', {
			'is-visible': footer
		})

		const detachedFooterClass = classnames(c.detachedfooter, 'ui-modal-detached-footer', {
			'is-visible': detachedFooter
		})

		return (
			<div id={id} className={cx}>
				<div
					onClick={this.props.onBackdropClick}
					className={backdropClass}/>
				<div className={contentClass}>
					<div className={headerClass}>
						<span className='title'>  {title} </span>
					</div>
					<div className={bodyClass}>
						{children}
					</div>
					<div className={footerClass}>
						Footer here
					</div>
				</div>
				<div className={detachedFooterClass} onClick={this.props.onDetachedFooterClick}>
					{
						this.props.uploadPercent > 0 &&
						<div className="progress" style={{position: 'absolute', top: '10px', left: '0', width: '100%'}}>
							<div className="progress-bar" style={{width: this.props.uploadPercent + '%'}}></div>
						</div>
					}
					<span className='text'>{detachedFooterText}</span>
				</div>
			</div>
		)
	}
}

export default withStyles(c)(UIModal)
