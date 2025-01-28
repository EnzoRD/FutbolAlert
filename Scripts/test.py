from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv()

# Acceder a las variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

print(f"SID: {account_sid}")
print(f"Token: {auth_token}")