from fastapi import APIRouter
from api_v1.products.views import router as product_router

router = APIRouter()
router.include_router(router=product_router, prefix="/products")
