import React, { Component } from 'react';
import './app.css';

export default class App extends Component {

  render() {
    return (
      <div className="container">
        <h1>{"BIEN 470 Project"}</h1>
        <h2>{"Sequence Counter"}</h2>
        <form method="POST" action="/api/upload" encType="multipart/form-data">
          <input type="file" name="target_file" />
          <input type="file" name="target_file_2" />
          <input type="submit" value="Upload" />
        </form>
      </div>
    );
  }
}
