## Deployment

1. git clone both minimal, playground, brick-frontend, and genie-brickified repo into a same directory
2. cd into playground and `docker-compose up --build -d` (make sure the context is correct if not using `docker-compose` but `docker build` and make sure the `docker-compose` version is at least `v2`)
3. docker exec and `python -m brick_server.playground generate-jwt --user-id=admin --create` and authorize with it in the swagger UI
4. create domain and then init domain
5. through graphdb UI import ref-schema
6. upload .ttl
7. add domain user (current user e.g. admin) and create profile and assign argument
8. add app to site (create app) -> approve -> add to domain
9. user install app -> create app
10. install nvm and run brick-frontend (if node version, `yarn config set ignore-engines true`)
11. go to frontend (xxxx:3000), console `window.sessionStorage.setItem("token","{token}")`, refresh and use


## Play

`python -m brick_server.playground generate-jwt --user-id=admin --app-name=sb --domain=bldg --create-user`
