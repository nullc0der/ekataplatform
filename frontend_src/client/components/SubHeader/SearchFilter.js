import React from 'react'
import classnames from 'classnames'


class SearchFilter extends React.Component {
    state = {
        enabledFilters: this.props.enabledFilters
    }

    componentDidUpdate(prevProps) {
        if (prevProps.enabledFilters !== this.props.enabledFilters) {
            this.setState({
                enabledFilters: this.props.enabledFilters
            })
        }
    }

    handleDragStart = (e, name) => {
        e.dataTransfer.setData('text', name)
    }

    handleDragOver = (e) => {
        e.preventDefault()
    }

    handleDrop = (e, name) => {
        this.swapFilters(e.dataTransfer.getData('text'), name)
        e.dataTransfer.clearData()
    }

    handleDragEnter = (e, name) => {
        $(`#filter-${name}`).addClass('over')
    }

    handleDragLeave = (e, name) => {
        $(`#filter-${name}`).removeClass('over')
    }

    handleDragEnd = (e) => {
        for (const filter of this.state.enabledFilters) {
            $(`#filter-${filter}`).removeClass('over')
        }
    }

    swapFilters = (src, target) => {
        let swappedFilters = this.state.enabledFilters
        const temp = swappedFilters.indexOf(target)
        swappedFilters[swappedFilters.indexOf(src)] = target
        swappedFilters[temp] = src
        this.setState({
            enabledFilters: swappedFilters
        }, () => this.props.filterOrderChanged(swappedFilters))
    }

    render() {
        const {
            disabledFilters,
            changeSearchString,
            toggleFilterOptions,
            showFilterOptions,
            filterButtonClicked
        } = this.props

        const { enabledFilters } = this.state

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
                                        <div
                                            key={i}
                                            id={`filter-${x}`}
                                            draggable='true'
                                            onDrop={(e) => this.handleDrop(e, x)}
                                            onDragStart={(e) => this.handleDragStart(e, x)}
                                            onDragOver={this.handleDragOver}
                                            onDragEnter={(e) =>  this.handleDragEnter(e, x)}
                                            onDragLeave={(e) => this.handleDragLeave(e, x)}
                                            onDragEnd={this.handleDragEnd}
                                            className={classnames(
                                                "filter-button",
                                                {
                                                    "single": (i === enabledFilters.length - 1 && i % 2 === 0)
                                                })}
                                            onClick={(e) => filterButtonClicked(e, x)}>{x}</div>
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
                                            className={classnames(
                                                "filter-button", "is-disabled",
                                                {
                                                    "single": (i === disabledFilters.length - 1 && i % 2 === 0)
                                                })}
                                            onClick={(e) => filterButtonClicked(e, x)}>{x}</button>
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
