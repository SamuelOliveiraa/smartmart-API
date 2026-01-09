from app import database, models, routers
from fastapi import FastAPI

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartMart API")
app.include_router(routers.router)
