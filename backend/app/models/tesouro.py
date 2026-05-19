from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class TituloTesouro(Base):
    __tablename__ = "titulos_tesouro"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    vencimento: Mapped[str] = mapped_column(String(20))
    taxa_compra: Mapped[float] = mapped_column(Float)
    taxa_venda: Mapped[float] = mapped_column(Float)
    preco_compra: Mapped[float] = mapped_column(Float)
    preco_minimo: Mapped[float] = mapped_column(Float)
    coletado_em: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
