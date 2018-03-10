import React from 'react'
import classnames from 'classnames'


class PostGroupCard extends React.Component {
    render() {
        const {
            className
        } = this.props

        const cx = classnames(className, 'flex-vertical', 'post-group')

        return (
            <div className={cx}>
                <div className='date-area'>Mar 10, 2018</div>
                <div className='ui-post-group-card'>
                    <div className='post'>
                        <div className='header'>
                            <div className='avatar'></div>
                            <div className='info'>
                                <span className='username'>Prasanta Kakati</span>
                                <span className='time'>12:11</span>
                            </div>
                        </div>
                        <div className='content'>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc eu feugiat dui, nec placerat dolor. Donec vulputate tempor neque a facilisis. Integer ornare porta elit, non efficitur massa vehicula vitae. Nam rhoncus ornare dolor, id tincidunt turpis fermentum a. Mauris semper lectus diam, malesuada consequat elit tempus aliquam. Phasellus pulvinar tellus nec nulla feugiat, eget egestas lorem dictum. Cras facilisis, nisl non mattis ornare, enim quam cursus velit, id lacinia mauris ipsum vel mi. Phasellus volutpat eget sapien sit amet commodo.</div>
                    </div>
                    <div className='post'>
                        <div className='header'>
                            <div className='avatar'></div>
                            <div className='info'>
                                <span className='username'>Mark Witham</span>
                                <span className='time'>12:11</span>
                            </div>
                        </div>
                        <div className='content'>Morbi interdum commodo pharetra. Nullam tincidunt, eros non mattis semper, lorem arcu dignissim tellus, vitae blandit erat augue quis augue. Proin ut arcu nulla. Sed sed malesuada urna, vitae euismod dolor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum pharetra est id sem lacinia venenatis. Cras consequat dolor neque, non mattis eros imperdiet imperdiet. Morbi non ex vitae lectus rhoncus tincidunt sed non sapien. Mauris vel magna faucibus, feugiat urna non, sollicitudin tortor. Maecenas at blandit est. In at tortor ut tortor consectetur pulvinar nec id risus.</div>
                    </div>
                </div>
            </div>
        )
    }
}

export default PostGroupCard
