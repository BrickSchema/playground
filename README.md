
# Prep Stage

1. Run the frontend and register your account there.
2. Run `tools/prep.sh` using a command like this: `docker exec -it playground /app/tools/prep.sh $YOUR_EMAIL`
3. Get a JWT token for `admin` user and update `pytest.ini`
4. Update the HOSTNAME and ADMIN_ID in `pytest.ini`
5. Run pytest `pytest --ignore=tests/remote/app_hosting tests/remote/`.
6. Run the above again because of the dependencies across different pytest files.



# Helper Sripts

1. `docker exec -it playground /app/tools/upgrade_brick_users.py`: This upgrades existing Brick Server's users to Playground users.
2. `docker exec -it playground /app/tools/register_admin`: register a default admin. This admin is also used in test scripts.
3. `docker exec -it playground /app/tools/add_user_room <user_email>`: add bldg:RM101 to the given user. (Make sure your config file has base_ns as `bldg:` (instead of `bldg`).


`docker network connect isolated_nw playground`

Update user from the frontend to Playground using `tools/upgrade_brick_users.py`

- Activate all the apps per user manually: `tools/install_apps_for_user $USER_ID`

- To register metadatas, run `pytest brick-server-minimal/tests/remote/test_entities.py`. Note that you might need to remove `./brick-server-minimal/pytest.ini` to effect `./pytest.ini`


