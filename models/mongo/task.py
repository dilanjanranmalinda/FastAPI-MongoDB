from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField


class MongoTask(Document):
    meta = {'collection': 'tasks'}

    title = StringField(required=True)
    description = StringField(required=True)
    status = BooleanField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)
