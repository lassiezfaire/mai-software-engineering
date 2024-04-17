from product.model import Product
from products.model import Clothes
from bson import ObjectId

# product = Product(name='test6')

# print(product.create())

# print(Product.read_all())

# print(Product.read(id=ObjectId('661c6e00916f6f81cd61f75e')))

# print(Product.delete(id=ObjectId('661c6e00916f6f81cd61f75e')))

# clothes = Clothes(name='Fedora', type='hat', colour='Red')

# print(clothes.create())

print(Clothes.get_random())
