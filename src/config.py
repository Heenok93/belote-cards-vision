from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "vision" / "YOLO26_finetuned_best.pt"

DEFAULT_CONF = 0.25
DEFAULT_IMGSZ = 1024
DEFAULT_IOU = 0.65

APP_TITLE = "Card Vision AI"