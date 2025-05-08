from dotenv import load_dotenv
import os
import uvicorn
from main_server import app as server
load_dotenv()

# Verificar si las variables de entorno están cargadas
print("USER_POSTGRES:", os.getenv("USER_POSTGRES"))
print("DATABASE_POSTGRES:", os.getenv("DATABASE_POSTGRES"))
print("PASSWORD_POSTGRES:", os.getenv("PASSWORD_POSTGRES"))
print("BOT_API:", os.getenv("BOT_API"))
print("JWT_SECRET_KEY:", os.getenv("JWT_SECRET_KEY"))
# Si ejecutamos directamente, se inicia el servidor de Uvicorn
if __name__ == "__main__":
    # host="0.0.0.0" permite que el servidor sea accecible desde cualquier direccion ip
    # Definimos el puerto en el que se va a ejecutar el servidor
    #reload=True , permite que el servidor se reinicie automaticamnte cuando se dectecte cambios en el codigo
    uvicorn.run("main:server", host="0.0.0.0", port=8001, reload=True)