import time
from config import settings
from pydantic import BaseModel
import httpx
###
from apps.orders.models import BaseOrder

from apps.site.models import RequestCall


class TelegramBot(BaseModel):
	api_url: str = "https://api.telegram.org/bot"
	username: str
	access_token: str

	def send_msg(self, chat_id: str, msg: str):
		req_url = self.api_url + self.access_token + "/sendMessage"
		print('request url is', req_url)
		data = {
			"chat_id": chat_id,
			"text": msg,
			"parse_mode": "MarkdownV2",
		}
		resp = httpx.post(req_url, data = data)
		print('resp is', resp.json())

async def send_order_email(msg:str):
	pass

async def send_request_call_telegram(msg:str):
	group_id = settings.telegram_notif_group_id
	bot = TelegramBot(username=settings.telegram_bot_username, access_token=settings.telegram_bot_token)
	bot.send_msg(group_id, msg)

async def send_request_call(request_call: RequestCall):
	print('send admin notification run')
	msg = "📲 *Новая заявка на обратный звонок* ✨ \n"
	msg += f"Имя: *{request_call.name}* \n"
	msg += f"Номер телефона: *{request_call.phone_mask}* \n"

	# replace for telegram
	msg = msg.replace('-', '\-').replace('.', '\.').replace('=', '\=').replace('(','\(').replace(')','\)').replace('+', '\+')

	await send_request_call_telegram(msg=msg)
#	await send_order_email(msg=msg)
