const { spawn } = require('child_process'); // added
const express = require('express');
const fileUpload = require('express-fileupload');
const path = require('path');
const app = express();

app.use(fileUpload({}));

app.post('/api/upload', (req, res) => {
  console.log("Started");

  if (!req.files || Object.keys(req.files).length === 0) {
    console.log('no files')
    return res.status(400).send('No files were uploaded.');
  }

  // Accessing the file by the <input> File name="target_file"
  const targetFile = req.files.target_file;

  // mv(path, CB function(err))
  targetFile.mv(path.join(__dirname, 'uploads', targetFile.name), (err) => {
    if (err)
      return res.status(500).send(err);
  });

  let dataToSend;
  const seq = `./src/server/uploads/${targetFile.name}`; // instead of this, it would get the file from the request

  // spawn new child process to call the python script
  const python = spawn('python', ['./scripts/script1.py', seq]); // make sure script1.py is in same folder
  // collect data from script
  python.stdout.on('data', (data) => {
    console.log('Pipe data from python script ...');
    const str = data.toString();

    // mock code to "parse" the response
    /* const num = str.substr(13,1);
    const toReturn = {
      fullString: str,
      'num': num
    }; */

    // respond with the object
    // If we want to send the old page, can just send toReturn instead!
    dataToSend = data;
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    /* delete file code here */
    res.send(dataToSend);
  });

});

app.listen(process.env.PORT || 8080, () => console.log(`Listening on port ${process.env.PORT || 8080}!`));
