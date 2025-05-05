# Write an App

The folder `apps/demo` (https://github.com/BrickSchema/playground/tree/master/apps/demo) contains a demo app, which is a minimized read/write actuator with Brick and Playground
interfaces.

The demo app contains the following files:

```text
├── backend             # a simple backend written by express.js
│  └── index.js         
├── frontend            # a simple frontend in pure html
│  └── index.html       
├── build.sh            # a script that packs backend.zip and frontend.zip
├── Dockerfile          # sbos-playground uses the Dockerfile to build the image
├── package.json        # define the dependencies in the backend
└── yarn.lock           # lock the dependencies in package.json
```

You can use any language and framework to write the app backend and frontend.

## Backend

### Dockerfile

For the backend, you must provide a `Dockerfile` and other files (if necessary) to build the docker image.

For example, the `Dockerfile` of the demo app use `node 18` as base image, install the packages and run the backend file `backend/index.js`. For more information about how to write a `Dockerfile`, please refer to the official documentation of `Docker`.

!!! important
    You should start the backend server on `localhost:5000` in the docker image so that it can be accessed by the frontend.

```Dockerfile
FROM node:18-alpine

ENV HOME="/root"
WORKDIR /root

COPY ./package.json ./yarn.lock  /root/
RUN --mount=type=cache,target=/usr/local/share/.config/yarn/global yarn
COPY . /root

CMD node backend/index.js
```

### Get JWT (JSON Web Token)

When running the docker image, `playground` provides an environment variable `BRICK_SERVER_API_TOKEN`, which is a JWT (
JSON Web Token) to authorize the requests to the API endpoints in `playground`.

For example, the following code snippets get the JWT from the environment variable and parse the information in the JWT.

=== "Python"

    ```python
    import os
    import jwt
    api_token = os.environ.get('BRICK_SERVER_API_TOKEN')
    decoded_token = jwt.decode(api_token, options={"verify_signature": False})
    ```

=== "NodeJS"

    ```js
    const apiToken = process.env.BRICK_SERVER_API_TOKEN;    
    const decodedToken = JSON.parse(Buffer.from(apiToken.split('.')[1], 'base64').toString());
    ```

The decoded (parsed) JWT is a JSON object, which is in the format of

```json
{
  "sub": "user@example.com",
  "aud": [
    "brick"
  ],
  "domain": "Center_Hall",
  "app": "demo",
  "domain_user_app": "66c4ec995317281fb487ccd3",
  "exp": 1747595485
}
```

| Key             | Description                              |
|-----------------|------------------------------------------|
| sub             | User using this app                      |
| aud             | JWT audience (always "brick")            |
| domain          | The domain this app currently working in |
| app             | Name of this app                         |
| domain_user_app | ObjectId of this app instance in DB      |
| exp             | Expiration time of the JWT (Unix Epoch)  |

### Make API Requests to `playground`

The backend should add the JWT in the header as a bearer token when sending API requests to `playground`

```python
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer <JWT token>',
}
```

The base API endpoint of `playground` is https://brickserver.ucsd.edu/brickapi/v1/, you can also check https://brickserver.ucsd.edu/brickapi/v1/docs for a detailed documentation of the available APIs.



## Frontend

For the frontend, you must provide a `index.html` and other files (such as `js`, `css` files if necessary), and the folder will be served as static files on `playground`.
Though we only use a single html file as the frontend in the demo app, you can choose any frontend framework and use the build files as the frontend.

### Get JWT

When a user accesses the frontend through `playground`, the same JWT provided to the backend is included in the query parameter `token`. You can use `Javascript` to read the JWT.

```js
const baseURL = "https://brickserver.ucsd.edu/brickapi/v1/apps/api";
const params = new URL(document.location).searchParams;
const token = params.get("token");
```

### Make API Requests to Backend

`playground` designed special API endpoint translation rules for the frontend to access to backend APIs.
The base API endpoint for such API requests is https://brickserver.ucsd.edu/brickapi/v1/apps/api.

For example, if the backend has an API endpoint on `localhost:5000/example`, the frontend should send a request to https://brickserver.ucsd.edu/brickapi/v1/apps/api/example with the JWT in the header as a bearer token (same as how it is used in the backend).

## Submit the App

### Backend and Frontend Files

The backend and frontend files should be zipped into `backend.zip` and `frontend.zip` before submission. Make sure that the files are in the root of the zip archive.

For example, the structure of `backend.zip` in the demo app is 

```text
backend.zip
├── backend            
│  └── index.js         
├── Dockerfile          
├── package.json        
└── yarn.lock          
```

The structure of `frontend.zip` in the demo app is 

```text
frontend.zip
└── index.html       
```

The file `build.sh` is a helper script to generate these two zip files in the demo app.

### Permission Profile



