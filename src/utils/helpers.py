from pathlib import Path
import yaml


def get_project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parents[2]


def load_config() -> dict:
    """Load YAML configuration file."""
    project_root = get_project_root()
    config_path = project_root / "src" / "config" / "settings.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)