import os
from dotenv import load_dotenv

def get_secret():

     ENV = os.getenv("ENV", "development")
     load_dotenv(f".env.{ENV}")
     JWT_SECRET = os.getenv("JWT_SECRET")
     
     
     if not JWT_SECRET:
          raise ValueError("JWT_SECRET NOT FOUND")
     
     return JWT_SECRET

ALGORITHM = "HS256"