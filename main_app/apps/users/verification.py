from config import get_settings
import random

settings = get_settings()

def send_verification_sms_code(phone):
	# generate verification code
	otp = random.randint(1678, 8975)
	# code to send code to phone with call provider api
		# need to implement
	# if code is successfully send, return otp code
	return otp

