servidor-maestro-env\Scripts\activate.bat
pip install fastapi
pip install uvicorn
pip install requests
pip install python-dotenv
pip install pyjwt
pip install apscheduler
pip install psycopg2

sirve para convertir el pc en servidor
uvicorn --app-dir=.\src\server\ main:app --reload

-Librerias adicionales necesarias:
pip install telegram
pip install python-telegram-bot



Notas Miguel:

-Notas en 'keyword.py'
-Notas en 'token.py'
-cambios en helpers/jwt.py
-Añadida una variable de entorno 'TOKEN_BBDD'
-Asignada la variable 'TOKEN_BBDD' a 'token' en cada funcion del bot
