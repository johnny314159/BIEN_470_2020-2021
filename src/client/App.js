import React, { Component } from 'react';
import axios from 'axios';
import TreeChart from './components/TreeChart.js'
import './app.css';



export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
      done: false,
      data: '',
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    console.log(event.target.files[0]);
    this.setState({ value: event.target.files[0] });
  }

  handleSubmit(event) {
    /* add API call here */
    const formData = new FormData();
    formData.append('target_file', this.state.value);

    axios
      .post('/api/upload', formData)
      .then((res) => {
        console.log(res.data);
        this.setState({ done: true, data: res.data })
      })
      .catch((err) => {
        console.log(err);
        alert("File Upload Error")
      });
    event.preventDefault();
  }

  render() {
    if (this.state.done) {
      return(
        <div className="App"> <TreeChart data={this.state.data}/> </div>);
      /* <div className="App"> Success: {console.log(require("./tree_data.json"))}  </div>  {this.state.data}*/
    }
    else {
      return (
        <div className="App">
          <h1 className="App-header">
            BIEN470 project: RNA binding site prediction
          </h1>

          <form method="POST" encType="multipart/form-data" onSubmit={this.handleSubmit} >
            <input type="file" name="target_file" onChange={this.handleChange} />

            <input type="submit" value="Extract Orthologs & Boost Predictions"/>
          </form>

        </div>


      );
    }
  }
};
