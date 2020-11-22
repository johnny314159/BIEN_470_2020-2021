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
