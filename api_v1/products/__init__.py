from fastapi import APIRouter
from api_v1.products.views import router as product_router
from auth.demo_jwt_auth import router as auth_router_jwt
router = APIRouter()
router.include_router(router=product_router, prefix="/products")
router.include_router(router=auth_router_jwt, prefix="/JWT")
