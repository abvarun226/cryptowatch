import React from "react";
import { render } from "react-dom";
import _ from "lodash";

class RealTimePrice extends React.Component {
    constructor() {
        super();
        this.state = {
            data: [],
            loading: true
        };
        this.getPriceData = this.getPriceData.bind(this);
        this.handleClick = this.handleClick.bind(this);
        setTimeout(() => {
            this.getPriceData(this.state, null);
        }, 100);
        setInterval(() => {
            this.getPriceData(this.state, null);
        }, 10000);
    }

    getPriceData(state, instance) {
        this.setState({ loading: true });

        let url = "http://localhost/v1/current_price";
        fetch(url)
        .then(res => res.json())
        .then(
            (result) => {
                const res = {result};
                this.setState({
                    data: res.result,
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

    render() {
        const { data, loading } = this.state;
        return (
            <div>
                <button type="button" className="btn btn-info" onClick={this.handleClick}>Refresh</button><br /><br />
                <br />
                <div className="row">
                  <div className="col">
                    <div className="card" styles={{width: "15rem"}}>
                        <div className="card-body align-center">
                          <h4 className="card-title head-color">BTC</h4>
                          <h2 className="value-color">${data.btc}</h2>
                        </div>
                    </div>
                  </div>
                  <div className="col">
                    <div className="card" styles={{width: "15rem"}}>
                        <div className="card-body align-center">
                          <h4 className="card-title head-color">LTC</h4>
                          <h2 className="value-color">${data.ltc}</h2>
                        </div>
                    </div>
                  </div>
                  <div className="col">
                    <div className="card" styles={{width: "15rem"}}>
                        <div className="card-body align-center">
                          <h4 className="card-title head-color">Doge</h4>
                          <h2 className="value-color">${data.doge}</h2>
                        </div>
                    </div>
                  </div>
                  <div className="col">
                    <div className="card" styles={{width: "15rem"}}>
                        <div className="card-body align-center">
                          <h4 className="card-title head-color">ETH</h4>
                          <h2 className="value-color">${data.eth}</h2>
                        </div>
                    </div>
                  </div>
                </div>
            </div>
        );
    }
}

render(<RealTimePrice />, document.getElementById("root"));
