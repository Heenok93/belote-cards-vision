from dataclasses import dataclass
import cv2
import numpy as np


@dataclass
class ImageQualityReport:
    brightness: float
    contrast: float
    blur_score: float
    overexposed_pct: float
    underexposed_pct: float
    quality_score: float
    risk_level: str
    issues: list[str]
    recommended_preprocessing: str
    suggested_modes: list[str]


def _decode_image(image_bytes: bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Image illisible ou format non supporté.")

    return image


def _clamp_score(value: float) -> float:
    return max(0.0, min(10.0, value))


def diagnose_image(image_bytes: bytes) -> ImageQualityReport:
    image = _decode_image(image_bytes)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    brightness = float(gray.mean())
    contrast = float(gray.std())
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    overexposed_pct = float(np.mean(gray > 245) * 100)
    underexposed_pct = float(np.mean(gray < 15) * 100)

    issues = []
    suggested_modes = []

    # Heuristiques adaptées à ton cas : cartes + reflets + coins petits
    if brightness > 190:
        issues.append("Luminosité élevée : risque de reflets ou zones brûlées.")
        suggested_modes.append("darken")

    if overexposed_pct > 5:
        issues.append(f"Surexposition détectée : {overexposed_pct:.1f}% de pixels très clairs.")
        suggested_modes.append("darken")

    if brightness < 60:
        issues.append("Image sombre : risque de perte de détail.")
        suggested_modes.append("clahe")

    if contrast < 35:
        issues.append("Contraste faible : les symboles peuvent être moins lisibles.")
        suggested_modes.append("clahe")

    if blur_score < 60:
        issues.append("Image très floue : le preprocessing ne récupérera pas toute l'information.")
    elif blur_score < 120:
        issues.append("Netteté moyenne : un léger sharpen peut aider.")
        suggested_modes.append("sharpen")

    suggested_modes = list(dict.fromkeys(suggested_modes))

    brightness_score = 10 - abs(brightness - 130) / 18
    contrast_score = contrast / 6
    blur_quality_score = blur_score / 18
    exposure_penalty = overexposed_pct * 0.35 + underexposed_pct * 0.15

    quality_score = (
        0.30 * _clamp_score(brightness_score)
        + 0.25 * _clamp_score(contrast_score)
        + 0.30 * _clamp_score(blur_quality_score)
        + 0.15 * _clamp_score(10 - exposure_penalty)
    )

    quality_score = round(_clamp_score(quality_score), 1)

    if quality_score >= 7.5:
        risk_level = "low"
    elif quality_score >= 5.0:
        risk_level = "medium"
    else:
        risk_level = "high"

    if not issues:
        issues.append("Image globalement correcte pour l'inférence.")

    recommended_preprocessing = "auto" if suggested_modes else "none"

    return ImageQualityReport(
        brightness=round(brightness, 1),
        contrast=round(contrast, 1),
        blur_score=round(blur_score, 1),
        overexposed_pct=round(overexposed_pct, 1),
        underexposed_pct=round(underexposed_pct, 1),
        quality_score=quality_score,
        risk_level=risk_level,
        issues=issues,
        recommended_preprocessing=recommended_preprocessing,
        suggested_modes=suggested_modes,
    )