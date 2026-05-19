from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tesouro import TituloTesouro


async def create(db: AsyncSession, dados: dict) -> TituloTesouro:
    titulo = TituloTesouro(**dados)
    db.add(titulo)
    await db.commit()
    await db.refresh(titulo)
    return titulo


async def create_many(db: AsyncSession, lista: list[dict]) -> list[TituloTesouro]:
    titulos = [TituloTesouro(**d) for d in lista]
    db.add_all(titulos)
    await db.commit()
    return titulos


async def get_by_id(db: AsyncSession, id: int) -> TituloTesouro | None:
    result = await db.execute(select(TituloTesouro).where(TituloTesouro.id == id))
    return result.scalar_one_or_none()


async def get_all(db: AsyncSession) -> list[TituloTesouro]:
    result = await db.execute(select(TituloTesouro).order_by(TituloTesouro.coletado_em.desc()))
    return list(result.scalars().all())


async def get_by_nome(db: AsyncSession, nome: str) -> list[TituloTesouro]:
    result = await db.execute(
        select(TituloTesouro)
        .where(TituloTesouro.nome.ilike(f"%{nome}%"))
        .order_by(TituloTesouro.coletado_em.desc())
    )
    return list(result.scalars().all())


async def delete_by_id(db: AsyncSession, id: int) -> bool:
    titulo = await get_by_id(db, id)
    if not titulo:
        return False
    await db.delete(titulo)
    await db.commit()
    return True