import shutil

from app.core.constants import FRAME_DIR, VIDEO_DIR


class CleanupService:
    def cleanup(self):

        shutil.rmtree(VIDEO_DIR, ignore_errors=True)
        shutil.rmtree(FRAME_DIR, ignore_errors=True)

        VIDEO_DIR.mkdir(parents=True, exist_ok=True)
        FRAME_DIR.mkdir(parents=True, exist_ok=True)
