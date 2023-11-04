from mongoengine import Document, StringField, FloatField, DateTimeField


class MongoProducts(Document):
    meta = {'collection': 'products'}

    product_name = StringField(required=True)
    created_at = DateTimeField(required=True)
    price = FloatField(required=True)
    description = StringField(required=False)
