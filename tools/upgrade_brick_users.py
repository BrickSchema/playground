#!/usr/bin/env python
import sys
sys.path.append("./brick-server-minimal")
sys.path.append("./")

from brick_server.models import User as BrickUser
from playground.models import User

for user in BrickUser.objects():
    new_user = User(**user.to_mongo())
    user.delete()
    new_user.save()
    #activated_apps = ListField(ReferenceField(App), default=[])
