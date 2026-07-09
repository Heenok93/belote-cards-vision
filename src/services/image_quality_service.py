"""
Image quality analysis service.

Provides heuristics to evaluate whether an image is suitable for YOLO
inference and recommends an appropriate preprocessing strategy.
"""

from dataclasses import dataclass

import cv2
import numpy as np


# =============================================================================
# Quality thresholds
# =============================================================================

IDEAL_BRIGHTNESS = 130

MAX_BRIGHTNESS = 190
MIN_BRIGHTNESS = 60

MIN_CONTRAST = 35

MIN_BLUR_SCORE = 60
SHARPEN_BLUR_THRESHOLD = 120

OVEREXPOSED_PIXEL_THRESHOLD = 245
UNDEREXPOSED_PIXEL_THRESHOLD = 15

# =============================================================================
# Quality score weights
# =============================================================================

BRIGHTNESS_WEIGHT = 0.30
CONTRAST_WEIGHT = 0.25
SHARPNESS_WEIGHT = 0.30
EXPOSURE_WEIGHT = 0.15


# =============================================================================
# Data model
# =============================================================================

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


# =============================================================================
# Private helpers
# =============================================================================

def _decode_image(image_bytes: bytes) -> np.ndarray:
    """Decode an image from raw bytes."""

    arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Image illisible ou format non supporté.")

    return image


def _clamp_score(value: float) -> float:
    """Clamp a score between 0 and 10."""

    return max(0.0, min(10.0, value))


def _compute_quality_score(
    brightness: float,
    contrast: float,
    blur_score: float,
    overexposed_pct: float,
    underexposed_pct: float,
) -> float:
    """Compute the global image quality score."""

    brightness_score = 10 - abs(brightness - IDEAL_BRIGHTNESS) / 18
    contrast_score = contrast / 6
    blur_quality_score = blur_score / 18

    exposure_penalty = (
        overexposed_pct * 0.35
        + underexposed_pct * 0.15
    )

    quality_score = (
        BRIGHTNESS_WEIGHT * _clamp_score(brightness_score)
        + CONTRAST_WEIGHT * _clamp_score(contrast_score)
        + SHARPNESS_WEIGHT * _clamp_score(blur_quality_score)
        + EXPOSURE_WEIGHT * _clamp_score(10 - exposure_penalty)
    )

    return round(_clamp_score(quality_score), 1)


def _compute_risk_level(score: float) -> str:
    """Return the estimated inference risk level."""

    if score >= 7.5:
        return "low"

    if score >= 5.0:
        return "medium"

    return "high"


# =============================================================================
# Public API
# =============================================================================

def diagnose_image(image_bytes: bytes) -> ImageQualityReport:
    """
    Analyse an image and estimate its suitability for YOLO inference.
    """

    image = _decode_image(image_bytes)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    brightness = float(gray.mean())
    contrast = float(gray.std())
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    overexposed_pct = float(
        np.mean(gray > OVEREXPOSED_PIXEL_THRESHOLD) * 100
    )

    underexposed_pct = float(
        np.mean(gray < UNDEREXPOSED_PIXEL_THRESHOLD) * 100
    )

    issues: list[str] = []
    suggested_modes: list[str] = []

    # -------------------------------------------------------------------------
    # Heuristics
    # -------------------------------------------------------------------------

    if brightness > MAX_BRIGHTNESS:
        issues.append(
            "Luminosité élevée : risque de reflets ou zones brûlées."
        )
        suggested_modes.append("darken")

    if overexposed_pct > 5:
        issues.append(
            f"Surexposition détectée : {overexposed_pct:.1f}% de pixels très clairs."
        )
        suggested_modes.append("darken")

    if brightness < MIN_BRIGHTNESS:
        issues.append(
            "Image sombre : risque de perte de détail."
        )
        suggested_modes.append("clahe")

    if contrast < MIN_CONTRAST:
        issues.append(
            "Contraste faible : les symboles peuvent être moins lisibles."
        )
        suggested_modes.append("clahe")

    if blur_score < MIN_BLUR_SCORE:
        issues.append(
            "Image très floue : le preprocessing ne récupérera pas toute l'information."
        )

    elif blur_score < SHARPEN_BLUR_THRESHOLD:
        issues.append(
            "Netteté moyenne : un léger sharpen peut aider."
        )
        suggested_modes.append("sharpen")

    suggested_modes = list(dict.fromkeys(suggested_modes))

    quality_score = _compute_quality_score(
        brightness,
        contrast,
        blur_score,
        overexposed_pct,
        underexposed_pct,
    )

    risk_level = _compute_risk_level(quality_score)

    if not issues:
        issues.append(
            "Image globalement correcte pour l'inférence."
        )

    recommended_preprocessing = (
        "auto"
        if suggested_modes
        else "none"
    )

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