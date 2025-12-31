
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, logger
from fastapi.exceptions import RequestValidationError
from tortoise import Tortoise
from app.settings import TORTOISE_ORM

from app.routes import file_router, user_router
from app.exceptions import DrivaultException, StorageConfigurationException
from app.handlers import drivault_exception_handler, validation_exception_handler
from app.utils import Util

load_dotenv()

logger = logger.logger
debug = os.getenv("DEBUG", False)
reload = debug

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        Initialize Tortoise ORM on application startup and end the connection
        when server is stopped.
    """
    print("🟢 : Drivault Starting 🗄️")
    
    # Validate storage path before starting the server
    print("\n📁 Validating storage configuration...")
    try:
        global VALIDATED_STORAGE_PATH
        storage_path = os.getenv("FILE_STORAGE_PATH")
        VALIDATED_STORAGE_PATH = Util.validate_storage_path(storage_path, default_path="./uploads")
        print(f"✅ Storage path ready: {VALIDATED_STORAGE_PATH}\n")
    except PermissionError as e:
        print(f"\n{str(e)}")
        print("⚠️  Server will not start due to storage configuration error.\n")
        raise StorageConfigurationException(str(e))
    except Exception as e:
        print(f"\n❌ Unexpected error during storage validation: {str(e)}")
        print("⚠️  Server will not start due to storage configuration error.\n")
        raise StorageConfigurationException(str(e))
    
    url = TORTOISE_ORM.get("connections").get("default")
    model = {"models":TORTOISE_ORM.get("apps").get("models")}
    
    await Tortoise.init(
        db_url=url,
        modules=model,
    )
    await Tortoise.generate_schemas()
    print("✅ Database connected and schemas generated successfully!")
    yield
    # Clean up and release the resources
    print("Closing database connections...")
    await Tortoise.close_connections()
    print("Database connection is closed.")
    print("⚠️ : Server Shutdown process completed...")
    print("🫡 : GoodBye")

app = FastAPI(
    debug=os.getenv("DEBUG", False),
    title="My Personal Vault",
    version="1",
    lifespan=lifespan,
)

# Register exception handlers
app.add_exception_handler(DrivaultException, drivault_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/health")
async def health_check():
    return {"status": "Ok ✅"}

@app.get("/ping")
async def ping():
    return {"ping":"pong"}

app.include_router(
    router=file_router,
    prefix="/v1",
    tags=["Files"]
)
app.include_router(
    router=user_router,
    prefix="/v1",
    tags=["Auth"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        reload=True
    )
