# Central Finance

API REST para coleta, armazenamento e consulta de dados públicos de ativos financeiros brasileiros. O sistema busca informações diretamente de fontes oficiais e as disponibiliza em uma interface padronizada para consumo por aplicações frontend ou outros serviços.

---

## Objetivo

Centralizar em um único lugar dados de ativos financeiros disponíveis publicamente no Brasil — começando pelo Tesouro Direto —, eliminando a necessidade de acessar múltiplas fontes manualmente e viabilizando análises históricas de preços e taxas.

---

## Stack Técnica

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12+ |
| Framework | FastAPI |
| Package Manager | uv |
| ORM | SQLAlchemy (async) |
| Banco de Dados | SQLite + aiosqlite |
| Migrations | Alembic |
| HTTP Client | httpx |
| Validação de Config | pydantic-settings |

---

## Arquitetura

O backend segue o padrão **MVC** com separação clara de responsabilidades:

```
backend/
├── main.py                     # Entry point da aplicação
├── alembic.ini                 # Configuração do Alembic
├── pyproject.toml
├── .env                        # Variáveis de ambiente (não versionado)
├── .env.example                # Template de variáveis
├── migrations/
│   ├── env.py
│   └── versions/
└── app/
    ├── config.py               # Carregamento centralizado de settings
    ├── database.py             # Engine, sessão e Base declarativa
    ├── models/
    │   └── tesouro.py          # Model ORM + schema da tabela
    ├── routers/
    │   └── tesouro.py          # Endpoints HTTP
    ├── controllers/
    │   └── tesouro.py          # Lógica de negócio e orquestração
    └── services/
        ├── tesouro_direto.py   # Integração com fonte de dados externa
        └── tesouro_crud.py     # Operações de leitura e escrita no banco
```

### Fluxo de uma requisição

```
Request HTTP
    │
    ▼
routers/tesouro.py          → recebe e valida a requisição HTTP
    │
    ▼
controllers/tesouro.py      → aplica regras, orquestra os services
    │
    ├──▶ services/tesouro_direto.py   → busca dados na fonte externa
    │
    └──▶ services/tesouro_crud.py     → lê ou grava no banco de dados
              │
              ▼
         models/tesouro.py   → define o schema da tabela (Pydantic + SQLAlchemy)
              │
              ▼
         Response JSON
```

---

## Fonte de Dados

### Tesouro Direto

| Campo | Valor |
|---|---|
| Fonte | Tesouro Transparente (gov.br) |
| URL | `https://www.tesourotransparente.gov.br` |
| Formato | CSV com separador `;` |
| Atualização | Diária |
| Autenticação | Não requerida |
| Histórico disponível | Desde 2002 |

Os dados são obtidos do arquivo público de preços e taxas do Tesouro Nacional, que contém o histórico completo de todos os títulos já ofertados na plataforma.

---

## Endpoints

Base URL: `http://localhost:8000`

Documentação interativa disponível em: `http://localhost:8000/docs`

### Tesouro Direto — `/tesouro`

| Método | Rota | Descrição | Parâmetros |
|---|---|---|---|
| `POST` | `/tesouro/coletar` | Busca dados na fonte oficial e salva no banco | `dias` (query, padrão: `30`) |
| `GET` | `/tesouro/` | Lista todos os títulos salvos no banco | — |
| `GET` | `/tesouro/buscar` | Filtra títulos por nome | `nome` (query, obrigatório) |
| `GET` | `/tesouro/{id}` | Retorna um título pelo ID | `id` (path) |
| `DELETE` | `/tesouro/{id}` | Remove um título pelo ID | `id` (path) |

#### Exemplos de uso

```bash
# Coleta os últimos 30 dias (padrão)
POST /tesouro/coletar

# Coleta os últimos 7 dias
POST /tesouro/coletar?dias=7

# Carrega histórico completo (uso consciente — pode gerar 170k+ registros)
POST /tesouro/coletar?dias=9999

# Lista todos os títulos salvos
GET /tesouro/

# Busca por nome
GET /tesouro/buscar?nome=IPCA

# Busca por ID
GET /tesouro/42

# Remove por ID
DELETE /tesouro/42
```

#### Exemplo de resposta — `GET /tesouro/42`

```json
{
  "id": 42,
  "nome": "Tesouro IPCA+",
  "vencimento": "2032-08-15",
  "data_referencia": "2026-05-19",
  "taxa_compra": 7.86,
  "taxa_venda": 7.94,
  "preco_compra": 4312.50,
  "preco_minimo": 43.12,
  "coletado_em": "2026-05-19T10:30:00"
}
```

---

## Modelo de Dados

### `titulos_tesouro`

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER (PK) | Identificador único |
| `nome` | VARCHAR(120) | Nome do título (ex: Tesouro IPCA+) |
| `vencimento` | VARCHAR(20) | Data de vencimento do título |
| `data_referencia` | VARCHAR(10) | Data do pregão |
| `taxa_compra` | FLOAT | Taxa de compra da manhã |
| `taxa_venda` | FLOAT | Taxa de venda da manhã |
| `preco_compra` | FLOAT | PU de compra da manhã |
| `preco_minimo` | FLOAT | PU base (mínimo) da manhã |
| `coletado_em` | DATETIME | Timestamp de inserção no banco |

**Constraint única:** `(nome, vencimento, data_referencia)` — evita duplicatas em coletas repetidas.

---

## Instalação e Execução

### Pré-requisitos

- Python 3.12+
- uv (`pip install uv`)

### Setup

```bash
# Clone o repositório
git clone <repo-url>
cd projeto/backend

# Crie o ambiente virtual e instale as dependências
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

uv add fastapi uvicorn httpx pydantic-settings sqlalchemy alembic aiosqlite

# Configure as variáveis de ambiente
cp .env.example .env

# Aplique as migrations
alembic upgrade head

# Inicie o servidor
uv run uvicorn main:app --reload
```

### Variáveis de Ambiente

```env
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
FRONTEND_URL=http://localhost:3000
TESOURO_URL=https://www.tesourotransparente.gov.br/ckan/dataset/.../download/PrecoTaxaTesouroDireto.csv
BCB_URL=https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json
DATABASE_URL=sqlite+aiosqlite:///./database.db
```

---

## Decisões de Projeto

**Por que SQLite?**
Para o estágio atual (desenvolvimento local, volume controlado), o SQLite elimina a necessidade de um servidor de banco de dados. A abstração via SQLAlchemy permite migrar para PostgreSQL apenas trocando a `DATABASE_URL`, sem alterações no código.

**Por que não usar a API do site do Tesouro Direto diretamente?**
O endpoint JSON do site (`tesourodireto.com.br`) não é uma API pública oficial e retorna 403 para requisições fora do navegador, mesmo com headers simulados. O CSV do Tesouro Transparente é a fonte oficial, estável e documentada pelo governo.

**Por que o parâmetro `dias` no `/coletar`?**
O CSV histórico contém mais de 170 mil registros desde 2002. Sem filtro, cada coleta inseriria o arquivo inteiro, tornando a operação computacionalmente custosa. O padrão de 30 dias cobre o uso cotidiano; o histórico completo pode ser carregado explicitamente quando necessário.

**Por que `on_conflict_do_nothing` no `create_many`?**
Coletas periódicas inevitavelmente tentarão inserir registros já existentes. O upsert silencioso evita erros e torna a operação idempotente — pode ser chamada múltiplas vezes sem efeitos colaterais.

---

## Próximos Passos

### Curto prazo
- [ ] Implementar endpoints de indicadores econômicos (Selic, CDI, IPCA) via API do Banco Central
- [ ] Adicionar agendamento automático de coleta com APScheduler ou Celery
- [ ] Implementar paginação nos endpoints de listagem
- [ ] Escrever testes unitários para services e controllers (pytest + pytest-asyncio)

### Médio prazo
- [ ] Desenvolver frontend em Next.js + TypeScript para visualização dos dados
- [ ] Adicionar suporte a CDBs e LCIs via scraping estruturado ou Open Finance
- [ ] Implementar cache em memória (Redis) para reduzir leituras repetidas ao banco
- [ ] Adicionar autenticação via JWT para endpoints de escrita

### Longo prazo
- [ ] Migrar banco de dados para PostgreSQL para deploy em produção
- [ ] Containerizar a aplicação com Docker e Docker Compose
- [ ] Implementar pipeline de CI/CD com GitHub Actions
- [ ] Adicionar suporte a dados da B3 (ações e FIIs) via API oficial

---

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Commit suas alterações (`git commit -m 'feat: descrição da feature'`)
4. Push para a branch (`git push origin feature/nome-da-feature`)
5. Abra um Pull Request

---

## Licença

MIT
