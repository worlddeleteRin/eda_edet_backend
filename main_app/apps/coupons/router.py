from fastapi import APIRouter, Request, HTTPException
from bson.json_util import loads, dumps
import json

import datetime

# models 
from .models import BaseCoupon

router = APIRouter(
	prefix = "/coupons",
	tags = ["coupons"],
)


@router.get("/")
async def create_coupon(
	request: Request,
	coupon: BaseCoupon,
	):

	return {
		"status": "success",
	}

@router.post("/")
async def create_coupon(
	request: Request,
	coupon: BaseCoupon,
	):

	print('coupon is', coupon)
	# need to check, if coupon with that id exists
	# add coupon to db
	request.app.coupons_db.insert_one(
		coupon.dict(by_alias=True)
	)
	return {
		"status": "success",
#		"products": products_result,
	}
