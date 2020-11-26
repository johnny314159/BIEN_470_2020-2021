const express = require('express');
const { spawn } = require('child_process'); // added
const upload = require('express-fileupload');

const os = require('os');

const app = express();

app.use(upload(undefined));

app.get('/', (req, res) => {
  res.sendFile(`${__dirname}/index.html`);
});

app.post('/', (req, res) => {
  if (req.files) {
    console.log(req.files);
    const file = req.files.file;
    const filename = file.name;
    console.log(filename);

    file.mv(`~/uploads/${filename}`, function (err) {
      if (err) {
        res.send(err);
      } else {
        res.send('File Uploaded');
      }
    });
  }
});

app.get('/api/runscript/', (req, res) => {
  let dataToSend;
  const seq = req.query.sequence; // instead of this, it would get the file from the request

  // spawn new child process to call the python script
  const python = spawn('python', ['./scripts/script1.py', seq]); // make sure script1.py is in same folder
  // collect data from script
  python.stdout.on('data', (data) => {
    console.log('Pipe data from python script ...');
    const str = data.toString();
    // mock code to "parse" the response
    const num = str.substr(13,1);
    const toReturn = {
      fullString: str,
      'num': num
    };
    // respond with the object
    dataToSend = toReturn;
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send(dataToSend);
  });
});

app.listen(process.env.PORT || 8080, () => console.log(`Listening on port ${process.env.PORT || 8080}!`));

app.listen(3000)
