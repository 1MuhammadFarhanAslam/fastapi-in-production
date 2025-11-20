from fastapi import FastAPI
# Note the import path uses the package name, confirming correct src-layout setup
from fastapi_mlops_template.core.config import settings

def create_application() -> FastAPI:
    """
    Initializes and configures the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    @app.get("/", tags=["Hello World"])
    async def root():
        """A simple entry point to confirm the service is running."""
        return {"message": "Hello World! Welcome to the FastAPI MLOps Template."}

    # Future routers will be attached here
    # from .api.root import api_router
    # app.include_router(api_router)
    
    # Future startup/shutdown events will be attached here
    # @app.on_event("startup")...

    return app

app = create_application()