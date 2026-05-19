import httpx
import csv
import io
from app.config import settings

HISTORICO_URL = "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv"


async def fetch_titulos() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(HISTORICO_URL, timeout=30)
        response.raise_for_status()

        content = response.content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content), delimiter=";")

        titulos = []
        for row in reader:
            titulos.append({
                "nome": row["Tipo Titulo"],
                "vencimento": row["Data Vencimento"],
                "taxa_compra": float(row["Taxa Compra Manha"].replace(",", ".")) if row["Taxa Compra Manha"] else None,
                "taxa_venda": float(row["Taxa Venda Manha"].replace(",", ".")) if row["Taxa Venda Manha"] else None,
                "preco_compra": float(row["PU Compra Manha"].replace(",", ".")) if row["PU Compra Manha"] else None,
                "preco_minimo": float(row["PU Base Manha"].replace(",", ".")) if row["PU Base Manha"] else None,
            })

        return titulos