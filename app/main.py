# app/main.py
import os
from dotenv import load_dotenv

# Cargar las variables del .env al inicio
load_dotenv()

import asyncio
from fastapi import FastAPI
from app.routes import drones, medications
from app.core.database import connect_to_mongo, close_mongo_connection
from app.services.battery_monitor import battery_monitor

app = FastAPI(
    title="Drones Dispatch API",
    description="API REST para la comunicación con un controlador de despacho de drones.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


    # Iniciar el monitor de batería
    await battery_monitor.start(interval_seconds=30)


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    # Detener el monitor de batería
    await battery_monitor.stop()

app.include_router(drones.router)
app.include_router(medications.router)
