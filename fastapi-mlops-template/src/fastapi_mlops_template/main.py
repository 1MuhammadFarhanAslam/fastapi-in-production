from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi_mlops_template.core.config import settings
from fastapi_mlops_template.services.ml_predictor import MLModelService
from fastapi_mlops_template.infrastructure.db_connection import Database
from fastapi_mlops_template.schemas.payload import PredictionPayload
from fastapi_mlops_template.schemas.response import TextPredictionResponse

# Global instances
ml_service = MLModelService(use_api=False)  # Using local inference to avoid API issues
db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    # await db.connect()  # Disabled until PostgreSQL is configured
    ml_service.load_model()
    
    # Store in state if you prefer dependency injection via Request
    app.state.ml_service = ml_service
    
    yield
    
    # --- Shutdown ---
    ml_service.unload_model()
    # await db.disconnect()  # Disabled until PostgreSQL is configured

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    @app.get("/")
    async def root():
        return {"message": "MLOps Template Running"}

    # --- EXAMPLE 1: PATH PARAMETER ---
    # URL: http://127.0.0.1:8000/hi/Farhan
    # "who" is part of the path structure.
    @app.get("/hi/{who}")
    def greet_path(who: str):
        return {"type": "Path Parameter", "message": f"Hello, {who}!"}

    # --- EXAMPLE 2: QUERY PARAMETER ---
    # URL: http://127.0.0.1:8000/hi?who=Farhan
    # "who" is NOT in the decorator string, so FastAPI detects it as a query param.
    @app.get("/hi")
    def greet_query(who: str):
        return {"type": "Query Parameter", "message": f"Hello, {who}!"}

    @app.post("/predict", response_model=TextPredictionResponse)
    async def predict(payload: PredictionPayload):
        return ml_service.predict(payload)

    return app

app = create_application()