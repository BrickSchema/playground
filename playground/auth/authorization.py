from brick_server.auth.authorization import parse_jwt_token
from brick_server.models import get_doc

from ..models import StagedApp, User


SEP = '^#$%'

def make_permission_key(user_id, app_name, entity_id):
    return user_id + SEP + app_name + SEP + entity_id


def check_permissions(entity_ids, user, app, permission_required):
    for entity_id in entity_ids:
        perm_key = make_permission_key(user.user_id, app.name, entity_id)
        perm = r.get(perm_key)
        if perm is None:
            raise exceptions.Unauthorized('The token does not have any permission over {0}'.format(entity_id))
        perm = perm.decode('utf-8')
        perm_type, perm_start_time, perm_end_time = decode_permission_val(perm)
        if permission_required not in perm_type:
            raise exceptions.Unauthorized('The token does not have `{0}` permission for {1}'.format(permission_required, entity_id))
        curr_time = time.time()
        if curr_time < perm_start_time or curr_time > perm_end_time:
            raise exceptions.Unauthorized('The token is not valid at the current time.')
    return True

def evaluate_app_user(action_type, target_ids, *args, **kwargs):
    jwt_payload = parse_jwt_token(kwargs['token'].credentials)
    app = get_doc(StagedApp, name=jwt_payload['app_id'])
    user  = get_doc(User, user_id=jwt_payload['user_id'])
    check_permissions(target_ids, user, app, action_type)
