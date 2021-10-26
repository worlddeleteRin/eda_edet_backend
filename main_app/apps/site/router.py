from fastapi import APIRouter, Depends, Request, Body, BackgroundTasks
from typing import Optional, List

from datetime import datetime, timedelta

from pymongo import ReturnDocument

import uuid

# import config (env variables)
from config import get_settings

from .models import PickupAddress, StockItem, MenuLink, MainSliderItem, RequestCall

from .delivery_pickup import get_pickup_addresses
from apps.payments.payments import get_payment_methods
from apps.delivery.delivery import get_delivery_methods

# request call
from apps.notifications.request_call import send_request_call

# order exceptions

router = APIRouter(
	prefix = "/site",
	tags = ["site"],
)

settings = get_settings()

@router.get("/pickup-addresses",
# response_model = List[PickupAddress]
)
def pickup_addresses(
	request: Request,
	):
	pickup_addresses = get_pickup_addresses(request.app.pickup_addresses_db)
	return pickup_addresses

@router.post("/pickup-addresses")
def add_pickup_address(
	request: Request,
	pickup_address: PickupAddress,
):
	pickup_address.save_db(request.app.pickup_addresses_db)
	return pickup_address.dict()

@router.get("/checkout-common-info")
def get_checkout_common_info(
	request: Request,
):
	delivery_methods = get_delivery_methods(request.app.delivery_methods_db)
	payment_methods = get_payment_methods(request.app.payment_methods_db)
	pickup_addresses = get_pickup_addresses(request.app.pickup_addresses_db)

	return {
		"delivery_methods": delivery_methods,
		"payment_methods": payment_methods,
		"pickup_addresses": pickup_addresses,
	}

@router.get("/stocks")
def get_stocks(
	request: Request
):
	stocks_dict = request.app.stocks_db.find({})
	stocks = [StockItem(**stock).dict() for stock in stocks_dict]
	return {
		"stocks": stocks,
	}
@router.post("/stocks")
def create_stock(
	request: Request,
	stock: StockItem,
):
	stock.save_db(request.app.stocks_db)
	return stock.dict()

@router.get('/common-info')
def get_common_info(
	request: Request,
):
	menu_links_cursor = request.app.menu_links_db.find({}).sort("display_order", 1)
	menu_links = [MenuLink(**menu_link).dict() for menu_link in menu_links_cursor]
	#print('menu links are', menu_links)
	location_address = "г. Ялта пгт Береговое ( Кастрополь) ул. Кипарисная 1 корпус 15"
	delivery_phone = "+79781740707"
	delivery_phone_display = "7 978 174 07 07"
	main_logo_link = request.app.settings.base_static_url + "main_logo.png"
	return {
		"main_logo_link": main_logo_link,
		"menu_links": menu_links,
		"location_address": location_address,
		"delivery_phone": delivery_phone,
		"delivery_phone_display": delivery_phone_display,
	}

@router.get('/main-sliders')
def get_common_info(
	request: Request,
):
	main_sliders_dict = request.app.main_sliders.find({}).sort("display_order", 1)
	main_sliders = [MainSliderItem(**main_slider).dict() for main_slider in main_sliders_dict]
	return main_sliders 

@router.post('/request-call')
def get_common_info(
	request: Request,
	request_call_info: RequestCall,
	background_task: BackgroundTasks,
):
	background_task.add_task(send_request_call, request_call_info)
	return {
		"success": True
	}
