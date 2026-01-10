from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import database, models, routers

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartMart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router)
