import shutil
from pathlib import Path

from app.core.constants import FRAME_DIR, VIDEO_DIR


class CleanupService:
    def cleanup(
        self,
        paths: list[Path] | None = None,
    ):
        if paths is not None:
            for path in paths:
                path.unlink(missing_ok=True)

            return

        shutil.rmtree(VIDEO_DIR, ignore_errors=True)
        shutil.rmtree(FRAME_DIR, ignore_errors=True)

        VIDEO_DIR.mkdir(parents=True, exist_ok=True)
        FRAME_DIR.mkdir(parents=True, exist_ok=True)
