import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import config
from .initialize import initialize_system
from .api.routes import router
from .utils.logger import get_logger
import asyncio
import signal
import sys

logger = get_logger(__name__)

app = FastAPI(
    title="NOVA-Synapse",
    description="Sistema adaptativo de asistencia virtual",
    version="1.0.0",
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    if not await initialize_system():
        logger.error("Error en la inicialización del sistema")
        sys.exit(1)

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    logger.info("Cerrando NOVA-Synapse...")
    # Implementar limpieza de recursos

def signal_handler(sig, frame):
    """Manejador de señales para cierre graceful"""
    logger.info(f"Señal recibida: {sig}")
    sys.exit(0)

def main():
    """Función principal de entrada"""
    # Registrar manejadores de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Configurar uvicorn
    uvicorn_config = {
        "app": "nova_synapse.main:app",
        "host": config.API_HOST,
        "port": config.API_PORT,
        "workers": config.API_WORKERS,
        "loop": "auto",
        "reload": config.DEBUG,
        "log_level": "debug" if config.DEBUG else "info",
        "proxy_headers": True,
        "forwarded_allow_ips": "*",
    }

    # Iniciar servidor
    try:
        uvicorn.run(**uvicorn_config)
    except Exception as e:
        logger.error(f"Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()