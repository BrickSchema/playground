# Initialization

In this guide, most of the operations should be done on the swagger API page.
If you do not change port settings, it should be on <http://localhost:9000/brickapi/v1/docs>.

## Register user

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

## Set superuser

Use the API `POST /brickapi/v1/users/init_superuser` to set the current user as superuser.
This API can only be called when no superuser exist in the system.


## Create domain

1.  Use the API `POST /brickapi/v1/domains/{domain}` to create a new domain.
    `domain` should be set to the name of the domain.
2.  