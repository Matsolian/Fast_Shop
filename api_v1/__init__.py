from fastapi import APIRouter

from .products.views import router as product_router
from .demo_auth import router as auth_router

router = APIRouter()
router.include_router(router=product_router)
router.include_router(router=auth_router)
