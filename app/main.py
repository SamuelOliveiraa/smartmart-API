from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import database, models, routers

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartMart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(routers.router)
