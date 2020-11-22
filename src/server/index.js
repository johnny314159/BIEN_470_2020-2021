const express = require('express');
const { spawn } = require('child_process'); // added
const os = require('os');

const app = express();

app.use(express.static('dist'));
// app.get('/api/getUsername', (req, res) => res.send({ username: os.userInfo().username }));

app.get('/api/runscript/', (req, res) => {
  let dataToSend;
  const seq = req.query.sequence;
  // spawn new child process to call the python script
  const python = spawn('python', ['./scripts/script1.py', seq]); // make sure script1.py is in same folder
  // collect data from script
  python.stdout.on('data', (data) => {
    console.log('Pipe data from python script ...');
    // mock code to "parse" the response
    const a = '1';
    const t = '2';
    const toReturn = {
      thing1: data.toString(),
      A: a,
      T: t
    };
    // respond with the object
    dataToSend = JSON.stringify(toReturn);
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    res.send(dataToSend);
  });
});

app.listen(process.env.PORT || 8080, () => console.log(`Listening on port ${process.env.PORT || 8080}!`));
