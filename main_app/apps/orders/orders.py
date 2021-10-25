from fastapi import Depends, Request
from .models import BaseOrder, BaseOrderCreate
from .order_exceptions import OrderNotExist
import uuid
from config import get_settings
from pydantic import UUID4
import pymongo

# from apps.users.models import UserDeliveryAddress
from apps.payments.payments import get_payment_method_by_id
from apps.delivery.delivery import get_delivery_method_by_id
from apps.site.delivery_pickup import get_pickup_address_by_id
from apps.users.user import get_user_delivery_address_by_id


settings = get_settings()

def get_order_by_id(orders_db, order_id: uuid.UUID, link_products = True):
	order = orders_db.find_one(
		{"_id": order_id}
	)
	if not order:
		raise OrderNotExist
	order = BaseOrder(**order)
	return order

def new_order_object(request: Request, new_order: BaseOrderCreate):
	exclude_fields = {"delivery_method", "payment_method", "delivery_address", "pickup_address"}
	order = BaseOrder(**new_order.dict(exclude=exclude_fields))
	order.payment_method = get_payment_method_by_id(request.app.payment_methods_db, new_order.payment_method)
	order.delivery_method = get_delivery_method_by_id(request.app.delivery_methods_db, new_order.delivery_method)
	if new_order.delivery_address:
		order.delivery_address = get_user_delivery_address_by_id(request.app.users_addresses_db, new_order.delivery_address)
	if new_order.pickup_address:
		order.pickup_address = get_pickup_address_by_id(request.app.pickup_addresses_db, new_order.pickup_address)
	return order

def get_orders_by_user_id(orders_db, user_id: UUID4):
	user_orders_dict = orders_db.find(
		{"customer_id": user_id}
	).sort("date_created", -1)
	if user_orders_dict.count() == 0:
		return []
	user_orders = [BaseOrder(**order).dict() for order in user_orders_dict]
	return user_orders
