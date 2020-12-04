import React, { Component } from 'react';
import './app.css';

export default class App extends Component {

  render() {
    return (
      <div className="App">
        <h1 className="App-header">
          <br/>
             BIEN470 project: Nucleotide-counting placeholder algorithm
          <br/>
          <br/>
          <br/>
          <br/>

          <form method="POST" action="/api/upload" encType="multipart/form-data">
            <input type="file" name="target_file" />
            <br/>
            <br/>
            <br/>
            <input type="submit" value="Parse nucleotides" />
          </form>

          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>
          <br/>

        </h1>
      </div>


    );
  }
}
