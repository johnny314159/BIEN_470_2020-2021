import React, { Component } from 'react';
import axios from 'axios';
import TreeChart from './components/TreeChart.js';
import BarChart from './components/BarChart.js';
import AboutData from './components/AboutData.js';
import Loader from 'react-loader';
import './app.css';


//lines=5&length=38&width=2&radius=10&scale=1.1&corners=0&speed=1.1&rotate=18&animation=spinner-line-fade-more&direction=1&color=%23ef0101&fadeColor=transparent&top=52&left=50&shadow=0%200%201px%20transparent&zIndex=2000000000&className=spinner&position=absolute
var loaderOptions = {
  color: '#57bdc3',
  lines: 7,
  length: 40,
  width: 3,
  radius: 15,
  scale: 1.1,
  corners: 0,
  speed: 1.0,
  rotate: 18,
  direction: 1,
  trail: 75,
  opacity: 0,
  fps: 5,
  zIndex: 2e9,
  top: '50%',
  left: '50%',
  shadow: false,
  hwaccel: true,
  position: 'absolute'
};


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
      done: false,
      data: '',
      loading: false
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }



  handleChange(event) {
    console.log(event.target.files[0]);
    this.setState({ value: event.target.files[0] });
  }

  handleSubmit(event) {
    this.setState({ loading: true })
    /* add API call here */
    const formData = new FormData();
    formData.append('target_file', this.state.value);

    axios
      .post('/api/upload', formData)
      .then((res) => {
        console.log(res.data[1]);
        this.setState({ done: true, data: res.data })
      })
      .catch((err) => {
        console.log(err);
        alert("File Upload Error")
      });
    event.preventDefault();
  }

  render() {
    /*Change the if statement here to pickup on a specific printed command?*/
    
    if (this.state.done) {
      return(

        <div className="RenderedApp"> 
          <h1>Results</h1>
          <div className="tree-container" style={{height: '90vh', marginLeft: '10vh'}}><TreeChart data={this.state.data[0]}/></div>
          <div className="bar-container" style={{height: '40vh'}}><BarChart data={this.state.data[1]}/></div>
          <div className="about-container" style={{height: '80vh'}}><AboutData data={this.state.data[1]}/></div>
          
          
        </div>
        );
      /* <div className="App"> Success: {console.log(require("./tree_data.json"))}  </div>  {this.state.data}*/
    }

    if (this.state.loading) {
      return(

        <div className="App">
          <h1 className="App-header">
            BIEN470 project: RNA binding site prediction
          </h1>
          Loading...

        
        <Loader options={loaderOptions}/>
        
        </div>

        );
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
