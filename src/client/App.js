import React, { Component } from 'react';
import axios from 'axios';
import TreeChart from './components/TreeChart.js'
import './app.css';

const treeData = require("./tree_data.json");

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
        this.setState({ done: true, data: res.data })
        console.log(res);
      })
      .catch((err) => alert("File Upload Error"));
    event.preventDefault();
  }

  render() {
    if (this.state.done) {
      return (
        <React.Fragment className="App">  <TreeChart data={treeData} /> </React.Fragment>
      )
    }
    else {
      return (
        <React.Fragment className="App">
          <h1 className="App-header">
            BIEN470 project: Nucleotide-counting placeholder algorithm
          </h1>

          <form method="POST" encType="multipart/form-data" onSubmit={this.handleSubmit} >
            <input type="file" name="target_file" onChange={this.handleChange} />

            <input type="submit" value="Parse nucleotides"/>
          </form>

        </React.Fragment>


      );
    }
  }
};
