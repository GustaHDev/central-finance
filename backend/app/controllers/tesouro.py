from sqlalchemy.ext.asyncio import AsyncSession
from app.services import crud_tesouro_direto, tesouro_direto
from app.models.tesouro import TituloTesouro


async def buscar_e_salvar(db: AsyncSession) -> list[TituloTesouro]:
    dados = await tesouro_direto.fetch_titulos()
    return await crud_tesouro_direto.create_many(db, dados)


async def listar(db: AsyncSession) -> list[TituloTesouro]:
    return await crud_tesouro_direto.get_all(db)


async def buscar_por_id(db: AsyncSession, id: int) -> TituloTesouro:
    titulo = await crud_tesouro_direto.get_by_id(db, id)
    if not titulo:
        raise ValueError(f"Título com id {id} não encontrado")
    return titulo


async def buscar_por_nome(db: AsyncSession, nome: str) -> list[TituloTesouro]:
    return await crud_tesouro_direto.get_by_nome(db, nome)


async def deletar(db: AsyncSession, id: int) -> None:
    deletado = await crud_tesouro_direto.delete_by_id(db, id)
    if not deletado:
        raise ValueError(f"Título com id {id} não encontrado")