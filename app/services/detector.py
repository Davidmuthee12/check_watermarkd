from pathlib import Path
import re

import cv2
import easyocr
import numpy as np

from app.core.constants import (
    OCR_CONFIDENCE_THRESHOLD,
    PLATFORM_WATERMARKS,
)


_reader: easyocr.Reader | None = None


def get_reader() -> easyocr.Reader:
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

    return _reader


class WatermarkDetector:
    """
    Detects watermark text from extracted video frames using
    OpenCV preprocessing + EasyOCR.
    """

    def __init__(self):
        self.reader = get_reader()

    def preprocess(self, frame_path: Path) -> np.ndarray:
        """
        Improves OCR accuracy by enhancing contrast and
        reducing background noise.
        """

        image = cv2.imread(str(frame_path))

        if image is None:
            raise ValueError(f"Unable to read frame {frame_path}")

        if len(image.shape) == 2:
            gray = image
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )

        enhanced = clahe.apply(gray)

        thresholded = cv2.adaptiveThreshold(
            enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            7,
        )

        return thresholded

    def watermark_regions(self, image: np.ndarray) -> list[np.ndarray]:
        height, width = image.shape[:2]
        half_height = max(height // 2, 1)
        half_width = max(width // 2, 1)
        band_height = max(height // 4, 1)

        return [
            image[:half_height, :half_width],
            image[:half_height, half_width:],
            image[half_height:, :half_width],
            image[half_height:, half_width:],
            image[height - band_height:, :],
        ]

    def normalize_text(self, text: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", " ", text.lower())
        return re.sub(r"\s+", " ", normalized).strip()

    def detect(self, frame_path: Path) -> list[str]:
        """
        Returns all detected platforms inside one frame.
        """

        processed = self.preprocess(frame_path)

        results = []

        for region in self.watermark_regions(processed):
            results.extend(
                self.reader.readtext(
                    region,
                    detail=1,
                    paragraph=False,
                )
            )

        detected = set()

        for _, text, confidence in results:
            if confidence < OCR_CONFIDENCE_THRESHOLD:
                continue

            normalized = self.normalize_text(text)

            for platform, keywords in PLATFORM_WATERMARKS.items():
                if any(keyword in normalized for keyword in keywords):
                    detected.add(platform)

        return sorted(detected)
