from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from core.models import db_helper, Product
from . import crud


async def product_by_id(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scooped_session_dependency),
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
