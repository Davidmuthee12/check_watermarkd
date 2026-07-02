from pathlib import Path

import cv2
import easyocr
import numpy as np

from app.core.constants import WATERMARK_IDENTIFIERS


class WatermarkDetector:
    """
    Detects watermark text from extracted video frames using
    OpenCV preprocessing + EasyOCR.
    """

    def __init__(self):
        # Loads the OCR model once when the service starts.
        self.reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

    def preprocess(self, frame_path: Path) -> np.ndarray:
        """
        Improves OCR accuracy by enhancing contrast and
        reducing background noise.
        """

        image = cv2.imread(str(frame_path))

        if image is None:
            raise ValueError(f"Unable to read frame {frame_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )

        enhanced = clahe.apply(gray)

        thresholded = cv2.threshold(
            enhanced,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]

        return thresholded

    def detect(self, frame_path: Path) -> list[str]:
        """
        Returns all detected platforms inside one frame.
        """

        processed = self.preprocess(frame_path)

        results = self.reader.readtext(
            processed,
            detail=1,
        )

        detected = set()

        for _, text, confidence in results:
            if confidence < 0.40:
                continue

            lower = text.lower()

            for keyword in WATERMARK_IDENTIFIERS:
                if keyword in lower:
                    detected.add(keyword.title())

        return sorted(detected)
