from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    app_name: str = "AI-Powered Multi-Disaster Monitoring & Resource Coordination System"
    version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    cors_origins: List[str] = ["*"]
    simulation_interval_sec: float = 4.0

settings = Settings()
