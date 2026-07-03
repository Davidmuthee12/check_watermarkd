# Check Watermarkd

Check Watermarkd is a FastAPI and Celery application that accepts a social media video URL, downloads the video, extracts representative grayscale frames with ffmpeg, and checks those frames for common platform watermark text using OpenCV preprocessing and EasyOCR.

## What It Detects

The detector currently maps OCR text to these platforms:

- TikTok
- CapCut
- Instagram
- Likee
- YouTube
- Snapchat

The keyword list lives in `app/core/constants.py` as `PLATFORM_WATERMARKS`.

## Application Flow

1. A client posts a video URL to `POST /video`.
2. `app/api/routers/video.py` validates the request and enqueues a Celery task.
3. `app/workers/tasks.py` creates a `VideoService` and runs the pipeline.
4. `VideoDownloader` uses `yt-dlp` to download the video into `storage/videos`.
5. `FrameExtractor` probes the video duration with `ffprobe`.
6. `FrameExtractor` runs one ffmpeg extraction pass that:
   - samples up to `MAX_EXTRACTED_FRAMES` frames,
   - scales frames to `FRAME_WIDTH`,
   - converts frames to grayscale,
   - writes frames into `storage/frames`.
7. `WatermarkDetector` loads or reuses the EasyOCR reader.
8. Each frame is preprocessed with OpenCV contrast enhancement and thresholding.
9. The detector scans watermark-heavy regions of each frame and matches OCR text against `PLATFORM_WATERMARKS`.
10. `VideoService` returns a `WatermarkResponse`.
11. Temporary files for that job are removed.
12. A client polls `GET /video/{job_id}` to read the Celery status and result.

## API

### Submit Video

```http
POST /video
Content-Type: application/json

{
  "video_url": "https://example.com/video"
}
```

Response:

```json
{
  "job_id": "celery-task-id"
}
```

### Check Status

```http
GET /video/{job_id}
```

Successful result:

```json
{
  "status": "SUCCESS",
  "result": {
    "watermarked": true,
    "detected_platforms": ["TikTok"],
    "processing_time": 42.18
  }
}
```

Failed result:

```json
{
  "status": "FAILURE",
  "result": {
    "error": "Unable to download video: ...",
    "type": "RuntimeError",
    "traceback": "..."
  }
}
```

## Core Modules

- `app/main.py`: creates the FastAPI application and API docs routes.
- `app/api/routers/video.py`: exposes video submission and job-status endpoints.
- `app/workers/celery.py`: configures Celery with Redis broker and result backend.
- `app/workers/tasks.py`: Celery task entry point for processing one video.
- `app/services/video.py`: orchestrates download, extraction, detection, timing, and cleanup.
- `app/services/downloader.py`: downloads social media videos with `yt-dlp`.
- `app/services/extractor.py`: extracts grayscale frames with `ffprobe` and `ffmpeg`.
- `app/services/detector.py`: preprocesses frames and detects watermark platform names.
- `app/services/cleanup.py`: removes job-specific temporary video and frame files.
- `app/core/constants.py`: storage paths, extraction settings, OCR threshold, and platform keyword mappings.

## Runtime Requirements

- Python environment with the packages from `requirements.txt`
- Redis running locally
- ffmpeg and ffprobe available on `PATH`
- A Celery worker process
- The FastAPI server

## Running Locally

Start Redis, then run the API:

```powershell
fastapi dev
```

Start the Celery worker in another terminal:

```powershell
celery -A app.workers.tasks worker --loglevel=info --pool=solo
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive docs are available at:

```text
http://127.0.0.1:8000/scalar
```

## Notes

- EasyOCR is initialized lazily after the video is downloaded and frames are extracted, so failed downloads do not pay the OCR startup cost.
- The OCR reader is reused inside the worker process after the first detection job.
- Some Instagram videos require cookies or login access. If `yt-dlp` cannot access a video, the Celery job returns a failure result.
- Detection accuracy depends on source video quality, watermark visibility, OCR confidence, and whether the platform watermark text appears in sampled frames.
