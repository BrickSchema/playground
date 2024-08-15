# Initialization

## Register admin user

=== "Username / Password"



=== "Google OAuth2"

    Before using this, ensure that [Google OAuth2](config/auth.md) has been setup in the configuration.

    Use the API `/brickapi/v1/auth/cookie/google/authorize` and it will return a json response in the format

    ```json
    {
      "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?foo=bar"
    }
    ```

    Open `authorization_url` in the browser and authorize with Google Account.
    The page will be redirected back to the [FRONTEND_URL](config/backend.md#frontend_url) entry in configuration.
    By default, it is the url of the Swagger API if not set in configuration.

!!! note

    The admin user can also be registered in the frontend.
    However, it is recommanded to use the Swagger API for convenience of debugging the setup.


