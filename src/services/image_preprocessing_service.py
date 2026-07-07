import cv2
import numpy as np

from src.services.image_quality_service import diagnose_image


def _decode_image(image_bytes: bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Image illisible ou format non supporté.")

    return image


def _encode_image(image) -> bytes:
    ok, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    if not ok:
        raise ValueError("Impossible d'encoder l'image prétraitée.")

    return buffer.tobytes()


def apply_clahe(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )

    l_channel = clahe.apply(l_channel)

    lab = cv2.merge((l_channel, a_channel, b_channel))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def apply_gamma(image, gamma: float):
    gamma = max(gamma, 0.1)
    inv_gamma = 1.0 / gamma

    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in range(256)
    ]).astype("uint8")

    return cv2.LUT(image, table)


def darken_image(image):
    # gamma > 1 dans cette implémentation assombrit légèrement
    return apply_gamma(image, gamma=0.75)


def brighten_image(image):
    return apply_gamma(image, gamma=1.25)


def apply_sharpen(image):
    kernel = np.array([
        [0, -0.6, 0],
        [-0.6, 3.4, -0.6],
        [0, -0.6, 0],
    ])

    sharpened = cv2.filter2D(image, -1, kernel)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def preprocess_image(image_bytes: bytes, mode: str = "auto") -> bytes:
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

        if report.brightness > 190 or report.overexposed_pct > 5:
            image = darken_image(image)

        if report.contrast < 40:
            image = apply_clahe(image)

        if 60 <= report.blur_score < 140:
            image = apply_sharpen(image)

    else:
        raise ValueError(f"Mode de preprocessing inconnu : {mode}")

    return _encode_image(image)