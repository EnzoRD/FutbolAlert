
import requests
from datetime import datetime, timedelta
import pytz
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Tu clave API
API_KEY = '0e04b607776d479681b2ed1e3d44e64e'

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

# Encabezados de autenticación
headers = {
    'X-Auth-Token': API_KEY
}

# Zona horaria de Argentina
argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")

def normalize_text(text):
    """Corrige problemas de encoding en nombres de equipos"""
    if isinstance(text, str):  
        return text.encode('ISO-8859-1', errors='replace').decode('utf-8', errors='replace')  
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

if __name__ == '__main__':
    all_matches = []

    # Obtener partidos de cada equipo
    for team, team_id in TEAM_IDS.items():
        matches = get_upcoming_matches(team, team_id)
        all_matches.extend(matches)

    # Ordenar los partidos por fecha
    all_matches.sort(key=lambda x: x["fecha"])

    # Mostrar resultados
    if all_matches:
        print(f"\n📅 Partidos programados desde {today} hasta {next_week}:")
        for match in all_matches:
            print(f"⚽ {match['equipo']} -> {match['local']} vs {match['visitante']} - Fecha (ARG): {match['fecha']}")
    else:
        print("\n❌ No hay partidos programados en la próxima semana.")


