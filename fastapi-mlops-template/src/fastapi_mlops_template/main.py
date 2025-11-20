from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Body, Header
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
    async def predict(payload: PredictionPayload = Body(embed=True)):
        """Use when you want just a string, wrapped in JSON object"""
        return ml_service.predict(payload)
    
    # Body() Examples
    
    # Example 1: Single value with Body()
    @app.post("/predict-simple")
    async def predict_simple(text: str = Body()):
        """Use when you want just a string, not wrapped in JSON object"""
        # Request: "Hello world" (just the string)
        payload = PredictionPayload(text=text)
        return ml_service.predict(payload)

    
    # Example 2: Body() with embed=True
    @app.post("/predict-embed")
    async def predict_embed(payload: PredictionPayload = Body(embed=True)):
        """Use when you want to wrap single model in JSON object"""
        # Request: {"payload": {"text": "Hello world"}}
        return ml_service.predict(payload)
    
    # Example 3: Multiple body parameters
    @app.post("/predict-advanced")
    async def predict_advanced(
        payload: PredictionPayload,
        confidence_threshold: float = Body(default=0.5),
        model_version: str = Body(default="v1")
    ):
        """Use when you need multiple separate values in request body"""
        # Request: {"text": "Hello", "confidence_threshold": 0.8, "model_version": "v2"}
        result = ml_service.predict(payload)
        # You can use confidence_threshold and model_version for processing
        return {"result": result, "threshold": confidence_threshold, "version": model_version}
    
    # HTTP Header Examples
    @app.get("/info")
    async def info(x_client_id: str = Header()):
        """Example of extracting custom HTTP header"""
        # Send as header: x-client-id: 12
        return {"client_id": x_client_id}
    
    # Query Parameter version
    @app.get("/info-query")
    async def info_query(x_client_id: str):
        """Example of query parameter"""
        # Send as query: ?x_client_id=12
        return {"client_id": x_client_id}
    
    # Optional Header
    @app.get("/info-optional")
    async def info_optional(x_client_id: str = Header(default=None)):
        """Example of optional header"""
        return {"client_id": x_client_id or "not_provided"}

    return app

app = create_application()