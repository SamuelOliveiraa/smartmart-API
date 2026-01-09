from fastapi import FastAPI

from app import database, models, routers

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartMart API")


# Rota de teste para você confirmar se está online
@app.get("/health")
def health_check():
    return {"status": "online", "database": "connected"}


app.include_router(routers.router)
