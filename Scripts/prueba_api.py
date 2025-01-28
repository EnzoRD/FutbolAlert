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


sys.stdout.reconfigure(encoding='utf-8')

# Configuración de Twilio desde el archivo .env
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
TO_WHATSAPP_NUMBER = os.getenv('TO_WHATSAPP_NUMBER')
API_KEY = os.getenv('API_KEY')


# Configuración de Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# IDs de los equipos
TEAM_IDS = {
    "Atlético de Madrid": 78,
    "Chelsea": 61
}

# Endpoint base de la API
BASE_URL = "http://api.football-data.org/v4/teams/{}/matches"

# Calcular el rango de fechas dinámicamente
today = datetime.now().strftime("%Y-%m-%d")
next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

# Parámetros de la consulta
params = {
    'status': 'SCHEDULED',
    'dateFrom': today,
    'dateTo': next_week
}

headers = {
    'X-Auth-Token': API_KEY
}

# Zona horaria de Argentina
argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")

def normalize_text(text):
    """Reemplaza caracteres especiales y normaliza la codificación"""
    import unicodedata
    if isinstance(text, str):
        text = text.encode("utf-8").decode("utf-8")  # Asegurar UTF-8
        text = unicodedata.normalize("NFKC", text)  # Normalizar caracteres
    return text


def convert_utc_to_argentina(utc_time):
    """Convierte el horario UTC a Argentina (UTC-3)"""
    utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")  # Convertir a datetime
    utc_dt = pytz.utc.localize(utc_dt)  # Marcarlo como UTC
    arg_dt = utc_dt.astimezone(argentina_tz)  # Convertir a Argentina
    return arg_dt.strftime("%Y-%m-%d %H:%M:%S")  # Formato legible

def get_upcoming_matches(team_name, team_id):
    """Obtiene los partidos programados para un equipo específico"""
    url = BASE_URL.format(team_id)

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            matches = response.json().get('matches', [])
            return [
                {
                    "equipo": team_name,
                    "local": normalize_text(match['homeTeam']['name']),
                    "visitante": normalize_text(match['awayTeam']['name']),
                    "fecha": convert_utc_to_argentina(match['utcDate'])
                }
                for match in matches
            ]
        else:
            print(f"⚠️ Error al obtener partidos de {team_name}: {response.status_code} - {response.reason}")
            print(f"Respuesta de la API: {response.json()}")  # Mostrar error detallado
            return []
    except Exception as e:
        print(f"❌ Ocurrió un error con {team_name}: {e}")
        return []

def send_whatsapp_message(body):
    """Envía un mensaje de WhatsApp usando Twilio"""
    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER,
            body=body
        )
        print(f"Mensaje enviado con SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error al enviar el mensaje: {e}")


if __name__ == '__main__':
    all_matches = []

    # Obtener partidos de cada equipo
    for team, team_id in TEAM_IDS.items():
        matches = get_upcoming_matches(team, team_id)
        all_matches.extend(matches)

    # Ordenar los partidos por fecha
    all_matches.sort(key=lambda x: x["fecha"])

    # Preparar el mensaje
    if all_matches:
        message_body = f"📅 Partidos programados desde {today} hasta {next_week}:\n"
        for match in all_matches:
            message_body += f"⚽ {match['equipo']} -> {match['local']} vs {match['visitante']} - Fecha (ARG): {match['fecha']}\n"
    else:
        message_body = "❌ No hay partidos programados en la próxima semana."
    
    # Enviar el mensaje por WhatsApp
    send_whatsapp_message(message_body)

