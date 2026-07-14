from pathlib import Path

# =============================================================================
# Project paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "models"

# =============================================================================
# Configuration files
# =============================================================================

AUTH_CONFIG_PATH = PROJECT_ROOT / "config" / "auth_config.yaml"

# =============================================================================
# Database
# =============================================================================

DATABASE_PATH = PROJECT_ROOT / "database" / "app.db"

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

# =============================================================================
# Dashboard UI
# =============================================================================

SCORE_SUMMARY_TITLE = "🏆 Score actuel"

APPLICATION_STATISTICS_TITLE = "📊 Statistiques"

TOTAL_GAMES_LABEL = "Parties"

COMPLETED_GAMES_LABEL = "Terminées"

ACTIVE_GAMES_LABEL = "En cours"

TOTAL_ROUNDS_LABEL = "Manches"

DETECTED_CARDS_LABEL = "Cartes détectées"

AVERAGE_SCORE_LABEL = "Score moyen"

RECENT_GAMES_TITLE = "🕘 Parties récentes"

MODEL_INFORMATION_TITLE = "🤖 Modèle IA"

LEADER_LABEL = "Leader"

DIFFERENCE_LABEL = "Écart"

ROUNDS_LABEL = "Manches"