from mongoengine import Document, StringField, DictField, ReferenceField, ListField, IntField

from brick_server.models import User as BrickUser


class MarketApp(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    permission_templates = DictField(DictField())
    token_lifetime = IntField(default=3600)

class App(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    app_id = StringField(required=True, unique=True)
    permission_templates = DictField(DictField())
    """
    Example:
    {
        "znt_query": {
            "query": "select ?znt where {?znt ?p ?o.};",
            "permission_type": "R",
        }
    }
    """
    result_storages = DictField(DictField(StringField()),
                                default={},
                                )

    #valid = BooleanField(required=True)
    #expiration_date = DateTimeField(required=True)
    #pending_approvals = DictField(ListField(), default=[]) # pending approvals from users. If approved, the itme goes to approvals
    #rejected_approvals = DictField(ListField()) # pending approvals from users. If approved, the itme goes to approvals
    #approvals = DictField(ListField())
    # In both of the above cases, key is query name and list of the values are the owner IDs.
    installer = StringField()
    #admin = StringField() # user_id
    callback_url = StringField()
    token_lifetime = IntField(default=3600)
    app_expires_at = IntField()
    permission_lifetime = IntField(default=36000)

class User(BrickUser):
    activated_apps = ListField(ReferenceField(App), default=[])
