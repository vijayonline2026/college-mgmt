from fastapi import FastAPI,APIRouter

app = FastAPI(
    title="College Management API",
    description="My FastAPI App",
    docs_url="/docs",
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "API is working 🚀"}

app.include_router(router, prefix="/api")
