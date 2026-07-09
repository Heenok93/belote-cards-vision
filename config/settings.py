from pathlib import Path

# =============================================================================
# Project paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "models"
DATABASE_DIR = PROJECT_ROOT / "src" / "database"

# =============================================================================
# Configuration files
# =============================================================================

AUTH_CONFIG_PATH = PROJECT_ROOT / "config" / "auth_config.yaml"

# =============================================================================
# Database
# =============================================================================

DATABASE_PATH = DATABASE_DIR / "app.db"

# =============================================================================
# YOLO model
# =============================================================================

DEFAULT_MODEL_PATH = MODELS_DIR / "vision" / "YOLO26_finetuned_best.pt"

DEFAULT_CONFIDENCE = 0.25
DEFAULT_IOU = 0.65
DEFAULT_IMAGE_SIZE = 1024

# =============================================================================
# Image upload
# =============================================================================

SUPPORTED_IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
)

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB