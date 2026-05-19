from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    tesouro_url: str = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsresult.json"
    bcb_url: str = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"
    database_url: str = "sqlite+aiosqlite:///./database.db"

    class Config:
        env_file = ".env"

settings = Settings()