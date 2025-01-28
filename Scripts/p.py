from twilio.rest import Client
import requests
from datetime import datetime, timedelta
import pytz
import sys
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# Cargar el archivo .env desde la ruta especificada
load_dotenv(dotenv_path, override=True)
print(f"TWILIO_ACCOUNT_SID: {os.getenv('TWILIO_ACCOUNT_SID')}")
print(f"TWILIO_AUTH_TOKEN: {os.getenv('TWILIO_AUTH_TOKEN')}")
print(f"TWILIO_WHATSAPP_NUMBER: {os.getenv('TWILIO_WHATSAPP_NUMBER')}")
print(f"TO_WHATSAPP_NUMBER: {os.getenv('TO_WHATSAPP_NUMBER')}")



