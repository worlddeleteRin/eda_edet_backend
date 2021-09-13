from fastapi import APIRouter, Depends, Request, Body
from typing import Optional, List

from datetime import datetime, timedelta

from pymongo import ReturnDocument

import uuid

# import config (env variables)
from config import settings

# helper methods from user app 
from apps.users.user import get_current_active_user
from apps.users.models import BaseUser

from .models import BaseOrder, BaseOrderCreate
from .orders import get_order_by_id, new_order_object

from apps.cart.cart import delete_session_cart



# order exceptions

router = APIRouter(
	prefix = "/orders",
	tags = ["orders"],
	# responses ? 
)


@router.get("/{order_id}")
def get_order(
	request: Request,
	order_id: uuid.UUID
	):
	order = get_order_by_id(request.app.orders_db, order_id)
	return order.dict()
@router.post("/")
def create_order(
	request: Request,
	new_order: BaseOrderCreate,
	current_user: BaseUser = Depends(get_current_active_user)
	):
	print('current user is', current_user)
	print('new order is', new_order)
	order: BaseOrder = new_order_object(request, new_order)
	print('order time is', order.date_created)
	# add products line_items to order
	for line_item in order.line_items:
		if line_item.product == None:
			order.add_line_item(request, line_item)
	# assign user to order, if user is simple user
	order.customer_id = current_user.id
	# add login to assign customer_id to passed customer_id to BaseOrderCreated, if user if admin,
	# and admin specifies the user, that need to be assigned to the order
	# count order amounts
	order.count_amount()
	# save order to db
	order.save_db(request.app.orders_db)

	# delete cart by session_id, if it is exist
	if new_order.customer_session_id:
		delete_session_cart(request.app.carts_db, new_order.customer_session_id)
	# delet cart by session_id, if it is exist
	# delete cart by cart_id, if it is specified in request
#	if order.cart_id:
#		cart = get_cart_by_id(request, order.cart_id, silent=True)
#		if cart:
#			cart.delete_db()
	return order.dict()

@router.post("/guest")
def create_guest_order(
	request: Request,
	new_order: BaseOrderCreate,
	):
	print('new order is', new_order)
	order: BaseOrder = new_order_object(request, new_order)
	print('order time is', order.date_created)
	# set order to guest order
	order.is_guest = True
	# add products line_items to order
	for line_item in order.line_items:
		if line_item.product == None:
			order.add_line_item(request, line_item)

	order.count_amount()
	# save order to db
	order.save_db(request.app.orders_db)
	# delete cart by session_id, if it is exist
	if new_order.customer_session_id:
		delete_session_cart(request.app.carts_db, new_order.customer_session_id)
	return order.dict()
