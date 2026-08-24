from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.pdf import router as pdf_router
from app.routes.image import router as image_router


app = FastAPI(
    title="Social Media Content Analyzer API",
    description=(
        "API for extracting and analyzing content "
        "from PDF and image files."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://social-media-content-analyzer-plum.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pdf_router)
app.include_router(image_router)


@app.get("/")
async def root():
    return {
        "message": "Social Media Content Analyzer API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }