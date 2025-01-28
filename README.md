# FutbolAlert ⚽

Un sistema automatizado para enviar notificaciones de partidos de fútbol programados a través de WhatsApp usando Twilio y una API de datos de fútbol. Ideal para fanáticos que quieren mantenerse al día con sus equipos favoritos. 🚀

---

## 📋 **Características**
- Consulta los próximos partidos programados para equipos específicos.
- Convierte horarios UTC a hora local (Argentina en este caso).
- Envía notificaciones por WhatsApp de manera automatizada usando Twilio.
- Automatización programada mediante `cron` en un servidor AWS EC2.
- Utiliza los logs del sistema (`cron`) para registrar las ejecuciones.

---

## 🚀 **Tecnologías utilizadas**
- **Python 3** (Lenguaje principal)
- **Twilio** (API para enviar mensajes de WhatsApp)
- **Football Data API** (Para obtener información de los partidos)
- **Python-dotenv** (Manejo de variables de entorno)
- **AWS EC2** (Servidor para ejecutar el script de forma automatizada)
- **Cron** (Para la automatización de tareas programadas)

---

## 🗂 **Estructura del proyecto**
```plaintext
FutbolAlert/
│
├── logs/                # Carpeta donde se guardan los logs de cron (se crea manualmente)
├── Scripts/             # Carpeta que contiene los scripts de Python
│   ├── prueba_api.py    # Script principal que consulta partidos y envía notificaciones
│   ├── test.py          # Script de pruebas
│
├── venv/                # Entorno virtual de Python
├── requirements.txt     # Dependencias necesarias para el proyecto
├── Info_teams_api.txt   # Información de los equipos (IDs)
├── .env                 # Archivo con variables de entorno sensibles (no se sube al repo)
├── README.md            # Documentación del proyecto (este archivo)
```

---

## 📦 **Instalación**
Sigue estos pasos para configurar el proyecto:

### 1⃣ **Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/FutbolAlert.git
cd FutbolAlert
```

### 2⃣ **Crear y activar un entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3⃣ **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4⃣ **Configurar las variables de entorno**
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```plaintext
TWILIO_ACCOUNT_SID=tu_sid_de_twilio
TWILIO_AUTH_TOKEN=tu_auth_token_de_twilio
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TO_WHATSAPP_NUMBER=whatsapp:+549XXXXXXXXXX
API_KEY=tu_api_key_de_football_data
```

### 5⃣ **Crear carpeta de logs para `cron`**
```bash
mkdir -p /home/ubuntu/FutbolAlert/logs
```

### 6⃣ **Probar el script**
Ejecuta el script principal para asegurarte de que funciona correctamente:
```bash
python3 Scripts/prueba_api.py
```

Si todo está bien, deberías recibir un mensaje de WhatsApp con los próximos partidos.

---

## 🕒 **Automatización con `cron`**
Para automatizar la ejecución, agrega una tarea en `crontab` que ejecute el script en los tiempos deseados.

### 🔢 **Ejemplo**: Ejecutar el script todos los lunes a las 8 AM hora de Argentina (11 AM UTC):
```bash
0 11 * * 1 /home/ubuntu/FutbolAlert/venv/bin/python3 /home/ubuntu/FutbolAlert/Scripts/prueba_api.py >> /home/ubuntu/FutbolAlert/logs/futbolAlert.log 2>&1
```

Guarda la configuración de `cron` con:
```bash
crontab -e
```

---

## ✨ **Personalización**
Puedes agregar más equipos a la consulta modificando el diccionario `TEAM_IDS` en `prueba_api.py`:

```python
TEAM_IDS = {
    "Atlético de Madrid": 78,
    "Chelsea": 61,
    "Real Madrid": 86,
    "Manchester United": 66
}
```

Luego, guarda y sube los cambios con `git push`.

---

## 🔓 **Debugging y Logs**
Para verificar los logs generados por `cron`, utiliza:

### Ver los logs recientes:
```bash
cat /home/ubuntu/FutbolAlert/logs/futbolAlert.log
```

### Ver los logs en tiempo real:
```bash
tail -f /home/ubuntu/FutbolAlert/logs/futbolAlert.log
```

### Ver errores de `cron` (si los hay):
```bash
sudo cat /var/log/syslog | grep CRON
```

---

## 📚 **Licencia**
Este proyecto está bajo la [Licencia MIT](https://opensource.org/licenses/MIT). Puedes usarlo, modificarlo y distribuirlo libremente.

---

## 👨‍💻 **Autor**
Creado con ❤️ por **[Enzo Ruiz Diaz](https://www.linkedin.com/in/enzo-ruiz-diaz/)**.

Si tienes preguntas o sugerencias, no dudes en contactarme a través de mi [Linkedin](https://www.linkedin.com/in/enzo-ruiz-diaz/).

---

## 🛠️ **Próximos pasos**
- Integrar más funcionalidades, como notificaciones en tiempo real.
- Añadir soporte para otras plataformas como Telegram.
- Mejorar la interfaz del script para que sea más interactiva.
⚽🎉
  


