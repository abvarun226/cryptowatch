import React from "react";
import { render } from "react-dom";
import _ from "lodash";

// Import React Table
import ReactTable from "react-table";
// import "react-table/react-table.css";

const defaultNumDays = 100;

class PriceHistory extends React.Component {
    constructor() {
        super();
        this.state = {
            data: [],
            numDays: defaultNumDays,
            loading: true
        };
        this.getPriceData = this.getPriceData.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.updateNumDays = this.updateNumDays.bind(this);
    }

    getPriceData(state, instance) {
        this.setState({ loading: true });

        let url = "http://localhost/v1/history?num_days=" + state.numDays;
        if (typeof(state.filtered) == "undefined") {
            url += "&type=all";
        } else if (state.filtered.length) {
            let crypto_type = state.filtered[0].value;
            url += "&type=" + crypto_type;
        }
        fetch(url)
        .then(res => res.json())
        .then(
            (result) => {
                const res = {result};
                this.setState({
                    data: res.result.data,
                    loading: false
                });
            },
            (error) => {
                this.setState({
                    loading: false,
                    error
                })
            }
        );
    }

    handleClick() {
        this.getPriceData(this.state, null);
    }

    updateNumDays(event) {
        this.setState({
            numDays: event.target.value
        });
    }

    render() {
        const { data, loading, numDays } = this.state;
        return (
            <div>
                <label for="numDays"># of Days: </label>
                <div class="input-group mb-3">
                    <input type="number" id="numDays" value={this.state.numDays} onChange={this.updateNumDays} placeholder="Number of days..." />
                    <button type="button" className="btn btn-info" onClick={this.handleClick}>Fetch Data!</button><br /><br />
                </div>
                <ReactTable
                    columns={[
                        {
                            Header: "Date",
                            accessor: "date",
                            filterable: false
                        },
                        {
                            Header: "Crypto",
                            accessor: "crypto_type",
                            filterable: true,
                            filterMethod: (filter, row) => {
                                if (filter.value == "all") {
                                    return true;
                                }
                                else {
                                    return row[filter.id] == filter.value;
                                }
                            },
                            Filter: ({ filter, onChange }) =>
                                <select
                                  onChange={event => onChange(event.target.value)}
                                  style={{ width: "100%" }}
                                  value={filter ? filter.value : "all"}
                                >
                                  <option value="all">All</option>
                                  <option value="btc">BTC</option>
                                  <option value="ltc">LTC</option>
                                  <option value="doge">Doge</option>
                                  <option value="eth">ETH</option>
                                </select>
                        },
                        {
                            Header: "Price (USD)",
                            accessor: "price",
                            filterable: false
                        },
                        {
                            Header: "Tx Volume",
                            accessor: "tx_volume",
                            filterable: false
                        }
                    ]}
                    data={data}
                    loading={loading}
                    onFetchData={this.getPriceData}
                    filterable
                    defaultPageSize={100}
                    numDays={numDays}
                    style={{
                      height: "700px"
                    }}
                    className="-striped -highlight"
                />
                <br />
            </div>
        );
    }
}

render(<PriceHistory />, document.getElementById("root"));
