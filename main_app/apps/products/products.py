from .models import BaseProduct
from .models import BaseCategory
from .product_exceptions import ProductNotExist, CategoryNotExist

from pydantic import UUID4

def get_product_by_id(products_db, product_id: UUID4, silent: bool = False):
	product = products_db.find_one(
		{"_id": product_id}
	)
	if not product:
		if not silent:
			raise ProductNotExist
		return None
	product = BaseProduct(**product)
	return product

def get_category_by_id(categories_db, category_id: UUID4, silent: bool = False):
	category = categories_db.find_one(
		{"_id": category_id }
	)
	if not category:
		if not silent:
			raise CategoryNotExist
		return None
	category = BaseCategory(**category)
	return category

