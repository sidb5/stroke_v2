import yaml
from pathlib import Path

def load_config():
    """Load configuration from config file."""
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f) 