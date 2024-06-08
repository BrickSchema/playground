# Initialization

## Register admin user

=== "Username / Password"

    

=== "Google OAuth2"
    
    Before using this, ensure that you have setup [Google OAuth2](config.md) in the configuration.

    Use the API `/brickapi/v1/auth/cookie/google/authorize` and the API will return a json response in the format
    
    ```json
    {
      "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?foo=bar"
    }
    ```
    
    Open `authorization_url` in the browser and continue with your google account. 
    The page will be redirected back to the `FRONTEND_URL` entry in configuration.
    By default, it is the url of the Swagger API if you didn't set it.

!!! note
    
    You can also register the admin user in the frontend. 
    We recommand to do it in the Swagger API for convenience of debugging the setup.    
    