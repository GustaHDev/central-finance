from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.controllers import tesouro as controller

router = APIRouter(prefix="/tesouro", tags=["Tesouro Direto"])


@router.post("/coletar", status_code=201)
async def coletar(db: AsyncSession = Depends(get_db)):
    try:
        titulos = await controller.buscar_e_salvar(db)
        return {"salvos": len(titulos), "titulos": titulos}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/")
async def listar(db: AsyncSession = Depends(get_db)):
    return await controller.listar(db)


@router.get("/buscar")
async def buscar_por_nome(nome: str, db: AsyncSession = Depends(get_db)):
    titulos = await controller.buscar_por_nome(db, nome)
    if not titulos:
        raise HTTPException(status_code=404, detail=f"Nenhum título encontrado para '{nome}'")
    return titulos


@router.get("/{id}")
async def buscar_por_id(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await controller.buscar_por_id(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{id}", status_code=204)
async def deletar(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await controller.deletar(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))