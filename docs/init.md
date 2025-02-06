# Initialization

In this guide, most of the operations should be done on the swagger API page.
If you do not change port settings, it should be on <http://localhost:9000/brickapi/v1/docs>.

## Setup User

### Register User

=== "Username / Password"

    1.  Use the API `POST /brickapi/v1/auth/register` to register user.
    
        `email`, `password` and `name` can be set in the request body.
    
        ```json
        {
          "email": "user@example.com",
          "password": "string",
          "name": "string"
        }
        ```
    
    2.  Use the API `POST /brickapi/v1/auth/cookie/login` to login the registered user with cookie.

        The `username` is same as the `email` set in the last step.


=== "Google OAuth2"

    Before using this, ensure that [Google OAuth2](config/auth.md) has been setup in the configuration.

    Use the API `GET /brickapi/v1/auth/cookie/google/authorize` and it will return a json response in the format

    ```json
    {
      "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?foo=bar"
    }
    ```

    Open `authorization_url` in the browser and authorize with Google Account.
    The page will be redirected back to the [FRONTEND_URL](config/backend.md#frontend_url) entry in configuration.
    By default, it is the url of the Swagger API if not set in configuration.

!!! info

    Use the API `GET /brickapi/v1/users/me` to check user is successfully registered and logined.
    

!!! note

    User can also be registered in the frontend.
    However, it is recommanded to use the Swagger API for convenience of debugging the setup.

### Set Superuser

Use the API `POST /brickapi/v1/users/init_superuser` to set the current user as superuser.
This API can only be called when no superuser exist in the system.


## Setup Domain

### Create Domain

1.  Use the API `POST /brickapi/v1/domains/{domain}` to create a new domain.

    `domain` should be set to the name of the domain.

2.  Use the API `GET /brickapi/v1/domains/{domain}/init` to init the domain.

    `domain` should be set to the name set in step 1.

3.  Use the API `GET /brickapi/v1/domains/{domain}/upload` to upload a `.ttl` file.

    An example file `center_hall.ttl` can be found in `projects/sbos-playground/examples/data/`.

!!! info
    
    The uploaded brick schema can be examined in the GraphDB GUI.
    By default, <http://127.0.0.1:37200/>.

### Add User to Domain

Use the API `POST /brickapi/v1/domains/{domain}/users/{user}` to add a user to a domain.

`domain` should be set to the domain name.

`user` should be set to the email of the user.



### Create User Profile

Use the API `POST /brickapi/v1/profiles/` to create a user profile.


!!! example

    ```json title="Request Body"
    {
      "name": "profile1",
      "read": "SELECT ?p WHERE {{ ?e brick:feeds {room} . ?e brick:hasPoint ?p . ?p a ?o . FILTER (?o IN (brick:Temperature_Sensor, brick:Occupancy_Sensor, brick:On_Off_Command, brick:CO2_Sensor, brick:Warm_Cool_Adjust_Sensor)) }}",
      "write": "SELECT ?p WHERE {{ ?e brick:feeds {room} . ?p brick:isPointOf ?e . ?p a brick:Warm_Cool_Adjust_Sensor .}}",
      "arguments": {
        "room": "brick:Room"
      }
    }
    ```

    A profile "profile1" will be created. The API will return 

    ```json title="Response Body"
    {
      "errorCode": "Success",
      "errorMessage": "",
      "showType": 0,
      "data": {
        "id": "<ObjectId>",
        "name": "profile1",
        "read": "SELECT ?p WHERE {{ ?e brick:feeds {room} . ?e brick:hasPoint ?p . ?p a ?o . FILTER (?o IN (brick:Temperature_Sensor, brick:Occupancy_Sensor, brick:On_Off_Command, brick:CO2_Sensor, brick:Warm_Cool_Adjust_Sensor)) }}",
        "write": "SELECT ?p WHERE {{ ?e brick:feeds {room} . ?p brick:isPointOf ?e . ?p a brick:Warm_Cool_Adjust_Sensor .}}",
        "arguments": {
          "room": "brick:Room"
        }
      }
    }
    ```
    
    Note that a profile is identified by its `id` (ObjectId), not by its `name`
    because there may exist duplicate profile names in the system.

!!! warning

    Currently, user profiles are shared among domains. It may be changed in future updates.

### Assign Profile to User

Use the API `POST /brickapi/v1/domains/{domain}/users/{user}/profiles` to assign a user profile to a domain user.

!!! example
    
    ```json title="Request Body"
    {
      "profile": "<ObjectId>",
      "arguments": {
        "room": "Center_Hall:101"
      }
    }
    ```
    
    Remember to use the profile id created in the last step.
    

## Setup App

### Create App

Use the API `POST /brickapi/v1/apps` to create an app.

!!! example

    ```json title="Request Body"
    {
      "name": "genie",
      "description": ""
    }
    ```

    An app "genie" will be created.

### Upload App Data

Use the API `POST /brickapi/v1/apps/{app}/submit` 
to submit frontend, backend, permission profile and permission model of an app.

!!! example

    | Form Argument    | Value |
    | -------- | ------- |
    | frontend_file | An archive (zip, tar) of the frontend files |
    | backend_file | An archive (zip, tar) of the backend files |
    | permission_profile_read   | `SELECT ?p WHERE {{ ?e brick:feeds {room} . ?e brick:hasPoint ?p . ?p a ?o . FILTER (?o IN (brick:Temperature_Sensor, brick:Occupancy_Sensor, brick:CO2_Sensor, brick:Warm_Cool_Adjust_Sensor)) }}` |
    | permission_profile_write  | `SELECT ?p WHERE {{ ?e brick:feeds {room} . ?e brick:hasPoint ?p . ?p a ?o . FILTER (?o IN (brick:On_Off_Command, brick:Warm_Cool_Adjust_Sensor)) }}`     |
    | permission_profile_arguments     | `{"room": "brick:Room",         "sensor": "brick:Temperature_Sensor", "setpoint": "brick:Temperature_Setpoint"}`    |
    | permission_model   | intersection |

### Approve App

An app need to be approved before it can be installed by users.

Use the API `POST /brickapi/v1/apps/{app}/approve` to approve it.

### Build App (by Docker)

The backend files of an app submitted before should contain a `Dockerfile`. 

Use the API `/brickapi/v1/apps/{app}/build` to build the app backend with the `Dockerfile`.

Please wait for a while because it takes some time to build the docker image.

!!! note
    
    A detailed build log is returned by the API. It can be used to verify whether the build succedded.

### Add App to Domain

Use the API `POST /brickapi/v1/domains/{domain}/apps/{app}` to approve the app in a domain 
(usually this step is done by a domain admin).

!!! note

    Use the API `GET /brickapi/v1/domains/{domain}/apps` to list all approved apps in a domain 
    and find whether the app is successfully added.

## Use App

### Install App

Use the API `POST /brickapi/v1/users/domains/{domain}/apps/{app}` to install an app for a user.

### Set App Arguments

Use the API `/brickapi/v1/users/domains/{domain}/apps/{app}` to set the arguments of an app for a user.

!!! example

    ```json title="Request Body"
    {
      "room": "Center_Hall:101",
      "sensor": "Center_Hall:AH-6.RA-T",
      "setpoint": "Center_Hall:AH-6.EFFHTG-SP"
    }
    ```

### Start App

Use the API `POST /brickapi/v1/users/domains/{domain}/apps/{app}/start` to start an app for a user.

A container named `sbos-playground-<app>-<user>-<id>` will be created and started. 
It should be listed in the `docker ps` command.


