import React from 'react'
import classnames from 'classnames'


class SearchFilter extends React.Component {
    render() {
        const {
            enabledFilters,
            disabledFilters,
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
                        <div className="selected-filters">
                            {
                                enabledFilters &&
                                enabledFilters.map((x, i) => {
                                    return (
                                        <button
                                            key={i}
                                            name={x}
                                            className={classnames(
                                                "filter-button",
                                                {
                                                    "single": (i === enabledFilters.length - 1 && i % 2 === 0)
                                                })}
                                            onClick={filterButtonClicked}>{x}</button>
                                    )
                                })
                            }
                        </div>
                        {
                            disabledFilters.length !== 0 &&
                            <div className="arrows-wrapper">
                                <div className="arrows">
                                    <i className="fa fa-angle-double-up"></i>
                                </div>
                            </div>
                        }
                        <div className="not-selected-filters">
                            {
                                disabledFilters &&
                                disabledFilters.map((x, i) => {
                                    return (
                                        <button
                                            key={i}
                                            name={x}
                                            className={classnames(
                                                "filter-button", "is-disabled",
                                                {
                                                    "single": (i === disabledFilters.length - 1 && i % 2 === 0)
                                                })}
                                            onClick={filterButtonClicked}>{x}</button>
                                    )
                                })
                            }
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default SearchFilter
