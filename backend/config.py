from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    max_pdf_size_mb: int = 20
    max_text_chars: int = 8000

    @property
    def max_pdf_bytes(self) -> int:
        return self.max_pdf_size_mb * 1024 * 1024

    class Config:
        env_file = ".env"


settings = Settings()
