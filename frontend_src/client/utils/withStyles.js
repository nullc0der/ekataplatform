import {Component} from 'react'
import withStylesIso from 'isomorphic-style-loader/lib/withStyles'

export default function withStyles(PassedComponent){
	return class WithStylesComponent extends Component {
		render(){
			const {ref, ...others} = this.props;
			return (
				<PassedComponent
					ref={this.handleRef}
					{...others}/>
		}
	}
}