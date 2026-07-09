from pathlib import Path
from tempfile import NamedTemporaryFile
import os

from ultralytics import YOLO

from config.settings import (
    DEFAULT_CONFIDENCE,
    DEFAULT_IMAGE_SIZE,
    DEFAULT_IOU,
    DEFAULT_MODEL_PATH,
)

from src.game.belote.cards import Suit, parse_card
from src.game.belote.scoring import TrumpMode, compute_score


# =============================================================================
# Model cache
# =============================================================================

_model: YOLO | None = None


# =============================================================================
# Model loading
# =============================================================================

def get_model(model_path: Path = DEFAULT_MODEL_PATH) -> YOLO:
    """Load the YOLO model only once."""

    global _model

    if not model_path.exists():
        raise FileNotFoundError(f"Modèle YOLO introuvable : {model_path}")

    if _model is None:
        _model = YOLO(str(model_path))

    return _model


# =============================================================================
# Detection post-processing
# =============================================================================

def deduplicate_detections_by_label(detections: list[dict]) -> list[dict]:
    """Keep only the highest-confidence detection for each card label."""

    best_by_label = {}

    for detection in detections:
        label = detection["label"]

        if (
            label not in best_by_label
            or detection["confidence"] > best_by_label[label]["confidence"]
        ):
            best_by_label[label] = detection

    return list(best_by_label.values())


# =============================================================================
# Image analysis
# =============================================================================

def analyze_image(
    image_bytes: bytes,
    trump_mode: TrumpMode,
    trump_suit: Suit | None = None,
    dix_de_der: bool = False,
    include_belote_rebelote: bool = True,
    confidence: float = DEFAULT_CONFIDENCE,
    image_size: int = DEFAULT_IMAGE_SIZE,
    iou: float = DEFAULT_IOU,
    deduplicate: bool = True,
) -> dict:
    """Run YOLO inference and compute the Belote score."""

    model = get_model()
    image_path = None

    if trump_mode == TrumpMode.CLASSIC and trump_suit is None:
        raise ValueError("trump_suit est obligatoire en mode CLASSIC.")

    if trump_mode is not TrumpMode.CLASSIC:
        trump_suit = None

    try:
        with NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(image_bytes)
            image_path = tmp.name

        results = model.predict(
            source=image_path,
            imgsz=image_size,
            conf=confidence,
            iou=iou,
            save=False,
            verbose=False,
        )

        result = results[0]
        names = model.names

        detections = []

        for box in result.boxes:
            class_id = int(box.cls[0])
            score = float(box.conf[0])
            label = names[class_id]
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            try:
                card = parse_card(label)
                valid = True
            except ValueError:
                card = None
                valid = False

            detections.append(
                {
                    "label": label,
                    "confidence": score,
                    "bbox": [x1, y1, x2, y2],
                    "card": card,
                    "valid": valid,
                }
            )

        raw_detections = detections.copy()

        if deduplicate:
            detections = deduplicate_detections_by_label(detections)

        cards = [d["card"] for d in detections if d["valid"]]

        score = compute_score(
            cards=cards,
            trump_mode=trump_mode,
            trump_suit=trump_suit,
            dix_de_der=dix_de_der,
            include_belote_rebelote=include_belote_rebelote,
        )

        annotated_image = result.plot()

        return {
            "score": score,
            "cards": cards,
            "detections": detections,
            "raw_detections": raw_detections,
            "n_detected": len(detections),
            "n_raw_detected": len(raw_detections),
            "n_valid_cards": len(cards),
            "annotated_image": annotated_image,
            "params": {
                "trump_mode": trump_mode.value,
                "trump_suit": trump_suit.value if trump_suit else None,
                "dix_de_der": dix_de_der,
                "include_belote_rebelote": include_belote_rebelote,
                "confidence": confidence,
                "image_size": image_size,
                "iou": iou,
                "deduplicate": deduplicate,
            },
        }

    finally:
        if image_path is not None and os.path.exists(image_path):
            os.remove(image_path)