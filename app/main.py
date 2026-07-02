from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.api.router import master_router

app = FastAPI()
app.include_router(master_router)


@app.get("/")
def root():
    return {"message": "welcome to check_watermarkd"}


### Scalar Documentation entry point
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
