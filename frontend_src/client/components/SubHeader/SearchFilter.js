import React from 'react'
import classnames from 'classnames'


class SearchFilter extends React.Component {
    render() {
        const {
            filters,
            enabledFilters,
            changeSearchString,
            toggleFilterOptions,
            showFilterOptions,
            filterButtonClicked
        } = this.props
        return (
            <div className="flex-horizontal">
                <div className="header-search-wrapper">
                    <input type="text" className="header-search-input" placeholder="Search here..." onChange={changeSearchString} />
                    <button className="header-search-button"><i className="fa fa-search"></i></button>
                </div>
                <button className="header-button" onClick={toggleFilterOptions}><i className="fa fa-filter"></i></button>
                <div className={classnames('filter-options', { 'is-open': showFilterOptions })}>
                    <div className="filter-options-header">
                        Filter Options
					</div>
                    <div className="flex-horizontal flex-wrap filter-options-content">
                        {
                            filters && 
                            filters.map((x, i) => {
                                return (
                                    <button 
                                        key={i}
                                        name={x}
                                        className={classnames(
                                            "filter-button",
                                            { 
                                                "is-disabled": !_.includes(enabledFilters, x),
                                                "single": (i === filters.length - 1 && i % 2 === 0)
                                            })}
                                        onClick={filterButtonClicked}>{x}</button>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
        )
    }
}

export default SearchFilter
