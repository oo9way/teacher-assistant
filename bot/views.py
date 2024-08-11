from django.shortcuts import render
from telegram import Update
from ninja import NinjaAPI
import json
from django.http import JsonResponse

from bot.dispatcher import dispatcher, bot
from dotenv import load_dotenv

load_dotenv()

webhook = NinjaAPI()


@webhook.post("/webhook")
def message_handler(request):
    update = Update.de_json(json.loads(request.body), bot)
    dispatcher.process_update(update)
    return JsonResponse({"ok": True})
