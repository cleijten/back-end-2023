__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
from datetime import datetime




def populate_test_database():


    #Create users

    models.User.create(
        name='Celia',
        address='Valkenlaar 23',
        zipcode='4854GR',
        city='Bavel',
        bank_account='NL12ABNA05891811854'
    
    )

    models.User.create(
        name='Aart',
        address='Valkenlaar 23',
        zipcode='4854GR',
        city='Bavel',
        bank_account='NL43RABO058340411854'    
   ) 
    
    #Create products

    models.Product.create(
        name = 'jeans',
        description = 'Vanguard jeans type 3000 size 34-32',
        price_per_unit = 156.99,
        qty_on_stock = 50
    )

    models.Product.create(
        name = 'pantalon',
        description = 'Only pantalon type mom size 46',
        price_per_unit = 49.99,
        qty_on_stock = 10
    )

    models.Product.create(
        name = 'sweater',
        description = 'Blue sweater with pme logo',
        price_per_unit = 69.99,
        qty_on_stock = 10
    )

    models.Product.create(
        name = 'hoody',
        description = 'Gestreepte hoody van wol',
        price_per_unit = 59.99,
        qty_on_stock = 12
    )


# Create Tags
models.Tag.create(name='broek')
models.Tag.create(name='trui')


# Create Product tags

models.ProductTag.create(product=1,tag=1)
models.ProductTag.create(product=2,tag=1)
models.ProductTag.create(product=3,tag=2)
models.ProductTag.create(product=4,tag=2)

# Create product owners

models.ProductOwner.create(product=1,owner=2, qty_owned=6)
models.ProductOwner.create(product=2,owner=1, qty_owned=2)
models.ProductOwner.create(product=3,owner=2, qty_owned=1)
models.ProductOwner.create(product=4,owner=1, qty_owned=4)



populate_test_database()


def search(term):
    term = term.lower()
    query=models.Product.select().where(models.Product.name.contains(term) | models.Product.description.contains(term))

    for product in query:
        print(product.name, product.description)

search('sweater')
search('jeans')


def list_user_products(user_id):
    
    query_1=(models.Product.select().join(models.ProductOwner).join(models.User).where(models.ProductOwner.owner == user_id))

    query_2 = models.User.select().where(models.User.id == user_id).get()

    username = query_2.name

    for item in query_1:
        print(f'{username} owns: {item.name}')

list_user_products(2)


def list_products_per_tag(tag_id):
  
    query_1 = (models.Product.select().join(models.ProductTag).join(models.Tag).where(models.ProductTag.tag == tag_id))

    query_2 = models.Tag.select().where(models.Tag.id == tag_id).get()
    tagname = query_2.name

    for item in query_1:
        print(f'{tagname} : {item.name}')

list_products_per_tag(2)


def add_product_to_catalog(user_id, product):

    query = models.Product.select().where(models.Product.name == product).get()
    productid = query.id
    models.ProductOwner.create(product=productid,owner=user_id, qty_owned=1)

add_product_to_catalog(2,'jeans')


def update_stock(product_id, new_quantity):
    product = models.Product.select().where(models.Product.id == product_id).get()
    old_stock = product.qty_on_stock
    product.qty_on_stock = new_quantity
    product.save()

    print(f'Previous stock of {product.name}: {old_stock}. New stock: {product.qty_on_stock}')


def purchase_product(product_id, buyer_id, quantity):
    product = models.Product.select().where(models.Product.id == product_id).get()
    buyer = models.User.select().where(models.User.id == buyer_id).get()


    if quantity >= product.qty_on_stock:
        print(f'Not enough of {product.name} on stock.')
        return

    total_price = round(product.price_per_unit * quantity, 2)
    
    transaction = models.PurchaseTransaction.create(
        buyer = buyer.id,
        product_bought = product.id,
        qty_bought = quantity,
        total_price = total_price,
        date_bought = datetime.now()
    )

    print(f'on {str(transaction.date_bought)} {buyer.name} bought {transaction.qty_bought} pieces of {product.name} at a total price of: {transaction.total_price}')

    new_quantity = product.qty_on_stock - quantity

    update_stock(product.id, new_quantity)

purchase_product(3,1,5)


def remove_product(product_id):
    product = models.Product.select().where(models.Product.id == product_id).get()

    print(f'{product.name} deleted')
    product.delete_instance()

remove_product(2)