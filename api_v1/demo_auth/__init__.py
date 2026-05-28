from fastapi import APIRouter
from api_v1.demo_auth.views import router as demoauth_router

router = APIRouter()
router.include_router(
    router=demoauth_router,
)
