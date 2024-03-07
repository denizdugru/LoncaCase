from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DecimalField,
    DateTimeField,
)


class Product(Document):
    stock_code = StringField(required=True)
    color = ListField(StringField())
    discounted_price = DecimalField(precision=2, required=False)
    images = ListField(StringField())
    is_discounted = BooleanField(default=False)
    name = StringField(required=True)
    price = DecimalField(required=True, precision=2)
    price_unit = StringField(default="USD")
    product_type = StringField(required=True)
    quantity = DecimalField(required=True)
    sample_size = StringField()
    series = StringField()
    status = StringField(default="Active")
    fabric = StringField()
    model_measurements = StringField()
    product_measurements = StringField()
    createdAt = StringField(required=True)
    updatedAt = StringField(required=True)
