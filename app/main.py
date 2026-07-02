from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # initialize OCR model later
    # initialize redis later

    yield

    # cleanup if necessary


app = FastAPI(
    title="Watermark Detector",
    lifespan=lifespan,
)

app.include_router(master_router)


@app.get("/")
async def root():
    return {"message": "welcome to check_watermarkd"}


@app.get("/scalar", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
