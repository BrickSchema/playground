const express = require('express')
const request = require('request');
const cors = require('cors')

const app = express()
const port = 5000

app.use(cors())

let apiToken = process.env.BRICK_SERVER_API_TOKEN;
if (!apiToken) {
  apiToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsaXV5aDk3MDYxNUBnbWFpbC5jb20iLCJhdWQiOlsiYnJpY2siXSwiZG9tYWluIjoiQ2VudGVyX0hhbGwiLCJhcHAiOiJnZW5pZSIsImRvbWFpbl91c2VyX2FwcCI6IjY2YzRlYzk5NTMxNzI4MWZiNDg3Y2NkMyIsImV4cCI6MTc0NzU5NTQ4NX0.Xa15aa5vBS1M9oQrdYvlFWYH07yftloyFSflFGAxFpg";
  // process.exit(-1);
}
const parseJwt = (token) => {
  return JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
}
const jwt = parseJwt(apiToken);
const domain = jwt.domain;
console.log(jwt)

const baseURL = "https://brickserver.ucsd.edu/brickapi/v1"
const listEntitiesURL = `${baseURL}/users/domains/${domain}/permissions`;
const readURL = `${baseURL}/actuation/domains/${domain}/read`;
const writeURL = `${baseURL}/actuation/domains/${domain}`;
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${apiToken}`,
}


app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.get('/list', (req, res) => {
  request.get(listEntitiesURL, {headers: headers}, (err, _res, body) => {
    res.send(body);
  });
})

app.get('/read', (req, res) => {
  const data = {
    [req.query.entity_id]: [""]
  }
  request.post(readURL, {headers: headers, json: data}, (err, _res, body) => {
    res.send(body);
  });
})

app.get('/write', (req, res) => {
  const data = {
    [req.query.entity_id]: [`${req.query.value}`]
  }
  request.post(writeURL, {headers: headers, json: data}, (err, _res, body) => {
    res.send(body);
  });
})


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
