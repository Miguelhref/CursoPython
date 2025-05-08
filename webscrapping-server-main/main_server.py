import os
import importlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.middlewares.fastApiErrorHandler import fastApiErrorHandler
from message_scheduler import message_scheduler
from src.repository.AmazonAsins import AmazonAsinsRepo
""" from bot_main import iniciar_bot  # Importamos el bot de Telegram """

app = FastAPI()

# Middleware para CORS
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# Manejo de errores
fastApiErrorHandler(app)

# Endpoint /ping (FastAPI)
@app.get("/ping")
def ping():
    return {"message": "pong"}

# Importar todas las rutas
print("Importing routes")
dir_routes = os.path.join(os.path.dirname(__file__), "src/routes")
files = os.listdir(dir_routes)
for file in files:
    if file.endswith(".py") and file != "__init__.py":
        route = importlib.import_module(f"src.routes.{file[:-3]}").router
        app.include_router(route)

# Inicializar repositorios
print("Initializing repository")
dir_repository = os.path.join(os.path.dirname(__file__), "src/repository")
files = os.listdir(dir_repository)

files.remove("Store.py")
files.remove("Token.py")
files.remove("Keyword.py")
files.remove("Product.py")

files.insert(0, "Store.py")
files.insert(1, "Token.py")
files.insert(2, "Keyword.py")
files.insert(3, "Product.py")

for file in files:
    if file.endswith(".py") and file != "__init__.py":
        getattr(importlib.import_module(f"src.repository.{file[:-3]}"), f"{file[:-3]}Repo").initialize()
print("Initializing Telegram scheduler")
message_scheduler.initialize_scheduler()

# Exportar la app FastAPI
export = app
