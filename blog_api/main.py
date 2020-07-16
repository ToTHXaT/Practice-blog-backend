from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api


app = FastAPI()

app.include_router(api, prefix="/api")
