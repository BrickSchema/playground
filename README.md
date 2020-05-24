

# Helper Sripts

1. `docker exec -it playground /app/tools/upgrade_brick_users.py`: This upgrades existing Brick Server's users to Playground users.
2. `docker exec -it playground /app/tools/register_admin`: register a default admin. This admin is also used in test scripts.


`docker network connect isolated_nw playground`

Update user from the frontend to Playground using `tools/upgrade_brick_users.py`

- Activate all the apps per user manually: `tools/install_apps_for_user $USER_ID`

