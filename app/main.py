from fastapi import FastAPI

from app import database, models, routers

# Cria tabelas no SQLite
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartMart API")

# Inclui os endpoints
app.include_router(routers.router)
