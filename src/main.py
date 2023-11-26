from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes import api_router
from config.settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    contact=settings.CONTACT,
    openapi_url=settings.OPEN_API_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT"),
    allow_headers=settings.CORS_HEADERS,
    expose_headers=[
        "Location",
    ],
)

# routers
app.include_router(api_router)


@app.get("/health", tags=["Health Check"])
async def health():
    return {"status": "ok"}
