
import os
import time
import jwt

from typing import Dict

JWT_SECRET = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = 'HS256'

def signJWT(payload) -> str:
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token

def create_access_token():
    return signJWT({ "client": True, "iat": time.time() })

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except:
        return None
'''
if __name__ == "__main__":
    token = create_access_token()
    print("Token JWT:", token)
'''
print("------------------------------------------------------")
print('TOKEN DE ACCESO A LA API:',create_access_token())
print("------------------------------------------------------")

