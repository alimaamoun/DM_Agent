"""
Core settings and configuration for the Content Automation System
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Ollama Configuration
    ollama_host: str = Field(default="http://localhost:11434", env="OLLAMA_HOST")
    ollama_no_gpu: bool = Field(default=False, env="OLLAMA_NO_GPU")
    
    # Hugging Face
    huggingface_token: Optional[str] = Field(default=None, env="HUGGINGFACE_TOKEN")
    
    # Google Drive Integration
    google_drive_credentials: Optional[str] = Field(default=None, env="GOOGLE_DRIVE_CREDENTIALS")
    google_drive_folder_id: Optional[str] = Field(default=None, env="GOOGLE_DRIVE_FOLDER_ID")
    
    # Social Media Platform APIs
    instagram_username: Optional[str] = Field(default=None, env="INSTAGRAM_USERNAME")
    instagram_password: Optional[str] = Field(default=None, env="INSTAGRAM_PASSWORD")
    twitter_api_key: Optional[str] = Field(default=None, env="TWITTER_API_KEY")
    twitter_api_secret: Optional[str] = Field(default=None, env="TWITTER_API_SECRET")
    twitter_access_token: Optional[str] = Field(default=None, env="TWITTER_ACCESS_TOKEN")
    twitter_access_secret: Optional[str] = Field(default=None, env="TWITTER_ACCESS_SECRET")
    
    # Content Generation Settings
    default_image_size: str = Field(default="1024x1024", env="DEFAULT_IMAGE_SIZE")
    max_caption_length: int = Field(default=2200, env="MAX_CAPTION_LENGTH")
    default_hashtag_count: int = Field(default=15, env="DEFAULT_HASHTAG_COUNT")
    
    # Scheduling
    content_schedule_timezone: str = Field(default="America/New_York", env="CONTENT_SCHEDULE_TIMEZONE")
    approval_email: Optional[str] = Field(default=None, env="APPROVAL_EMAIL")
    
    # Storage Paths
    local_asset_path: Path = Field(default=Path("./assets"), env="LOCAL_ASSET_PATH")
    output_path: Path = Field(default=Path("./output"), env="OUTPUT_PATH")
    temp_path: Path = Field(default=Path("./temp"), env="TEMP_PATH")
    
    # n8n Workflow Engine
    n8n_host: str = Field(default="http://localhost:5678", env="N8N_HOST")
    n8n_auth_user: str = Field(default="admin", env="N8N_AUTH_USER")
    n8n_auth_password: Optional[str] = Field(default=None, env="N8N_AUTH_PASSWORD")
    
    # Redis (for task queuing)
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Model Configuration  
    sd3_model_path: str = Field(default="stabilityai/stable-diffusion-3-medium-diffusers", env="SD3_MODEL_PATH")
    prompt_enhancer_model: str = Field(default="brxce/stable-diffusion-prompt-generator", env="PROMPT_ENHANCER_MODEL")
    caption_model: str = Field(default="llama3:latest", env="CAPTION_MODEL")
    text_model: str = Field(default="mistral:latest", env="TEXT_MODEL")
    
    # Development
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.local_asset_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()

# Utility functions
def get_image_size_tuple(size_str: str = None) -> tuple[int, int]:
    """Convert size string like '1024x1024' to tuple (1024, 1024)"""
    size_str = size_str or settings.default_image_size
    width, height = map(int, size_str.split('x'))
    return width, height

def get_device():
    """Get the appropriate device for model inference"""
    import torch
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu" 