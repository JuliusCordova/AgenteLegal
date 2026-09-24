from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("LEGAL_ENV", "local")
    log_level: str = os.getenv("LEGAL_LOG_LEVEL", "INFO")
    port: int = int(os.getenv("LEGAL_PORT", "8080"))
    gcp_project: str = os.getenv("LEGAL_GCP_PROJECT", "proyectopersonal-480420")
    gcp_region: str = os.getenv("LEGAL_GCP_REGION", "us-central1")
    model: str = os.getenv("LEGAL_MODEL", "")
    corpus_path: str = os.getenv("LEGAL_CORPUS_PATH", "data/raw")


settings = Settings()
