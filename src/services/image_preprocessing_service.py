"""
Image preprocessing service.

Applies image enhancement techniques before YOLO inference.
"""

import cv2
import numpy as np

from src.services.image_quality_service import (
    MAX_BRIGHTNESS,
    MIN_CONTRAST,
    MIN_BLUR_SCORE,
    SHARPEN_BLUR_THRESHOLD,
    diagnose_image,
)

# =============================================================================
# Preprocessing parameters
# =============================================================================

JPEG_QUALITY = 95

CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_SIZE = (8, 8)

DARKEN_GAMMA = 0.75
BRIGHTEN_GAMMA = 1.25

SHARPEN_KERNEL = np.array(
    [
        [0, -0.6, 0],
        [-0.6, 3.4, -0.6],
        [0, -0.6, 0],
    ]
)


# =============================================================================
# Image encoding / decoding
# =============================================================================

def _decode_image(image_bytes: bytes) -> np.ndarray:
    """Decode an image from raw bytes."""

    arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Image illisible ou format non supporté.")

    return image


def _encode_image(image: np.ndarray) -> bytes:
    """Encode an OpenCV image to JPEG."""

    ok, buffer = cv2.imencode(
        ".jpg",
        image,
        [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY],
    )

    if not ok:
        raise ValueError("Impossible d'encoder l'image prétraitée.")

    return buffer.tobytes()


# =============================================================================
# Preprocessing operations
# =============================================================================

def apply_clahe(image: np.ndarray) -> np.ndarray:
    """Apply CLAHE contrast enhancement."""

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=CLAHE_CLIP_LIMIT,
        tileGridSize=CLAHE_TILE_SIZE,
    )

    l_channel = clahe.apply(l_channel)

    lab = cv2.merge((l_channel, a_channel, b_channel))

    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def apply_gamma(image: np.ndarray, gamma: float) -> np.ndarray:
    """Apply gamma correction."""

    gamma = max(gamma, 0.1)
    inv_gamma = 1.0 / gamma

    table = np.array(
        [
            ((i / 255.0) ** inv_gamma) * 255
            for i in range(256)
        ]
    ).astype("uint8")

    return cv2.LUT(image, table)


def darken_image(image: np.ndarray) -> np.ndarray:
    """Darken an image."""

    return apply_gamma(image, DARKEN_GAMMA)


def brighten_image(image: np.ndarray) -> np.ndarray:
    """Brighten an image."""

    return apply_gamma(image, BRIGHTEN_GAMMA)


def apply_sharpen(image: np.ndarray) -> np.ndarray:
    """Apply a sharpening filter."""

    sharpened = cv2.filter2D(image, -1, SHARPEN_KERNEL)

    return np.clip(sharpened, 0, 255).astype(np.uint8)


# =============================================================================
# Public API
# =============================================================================

def preprocess_image(
    image_bytes: bytes,
    mode: str = "auto",
) -> bytes:
    """
    Apply image preprocessing before YOLO inference.
    """

    image = _decode_image(image_bytes)

    if mode == "none":
        return image_bytes

    if mode == "clahe":
        image = apply_clahe(image)

    elif mode == "darken":
        image = darken_image(image)

    elif mode == "brighten":
        image = brighten_image(image)

    elif mode == "sharpen":
        image = apply_sharpen(image)

    elif mode == "auto":

        report = diagnose_image(image_bytes)

        if (
            report.brightness > MAX_BRIGHTNESS
            or report.overexposed_pct > 5
        ):
            image = darken_image(image)

        if report.contrast < MIN_CONTRAST:
            image = apply_clahe(image)

        if (
            MIN_BLUR_SCORE
            <= report.blur_score
            < SHARPEN_BLUR_THRESHOLD
        ):
            image = apply_sharpen(image)

    else:
        raise ValueError(
            f"Mode de preprocessing inconnu : {mode}"
        )

    return _encode_image(image)