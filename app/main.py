from fastapi import FastAPI

from app import database, models, routers

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartMart API")

app.include_router(routers.router)
