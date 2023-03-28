from peewee import *

db = SqliteDatabase("betsy.db")

class BaseModel(Model):

    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    address = CharField()
    zipcode = CharField()
    city = CharField()
    bank_account = CharField()

class Product(BaseModel):
    name = CharField()
    description = TextField()
    price_per_unit = DecimalField(constraints=[Check('price_per_unit > 0')], decimal_places=2, auto_round=True)
    qty_on_stock = IntegerField()

class ProductOwner(BaseModel):
    owner = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    qty_owned = IntegerField()

class Tag(BaseModel):
    name = CharField()

class ProductTag(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)

class PurchaseTransaction(BaseModel):
    buyer = ForeignKeyField(User)
    product_bought = ForeignKeyField(Product)
    qty_bought = IntegerField()
    total_price = DecimalField(decimal_places=2, auto_round=True)
    date_bought = DateTimeField(formats='%d-%m-%Y')

db.connect()
# create db-tables as defined in models.py

def create_tables():
    with db:
        db.create_tables([
            User,
            Product,
            ProductOwner,
            Tag,
            ProductTag,
            PurchaseTransaction])

create_tables()
