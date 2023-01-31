from fastapi import APIRouter
from fastapi.responses import FileResponse
from PIL import Image
from fistbump.config import settings

router = APIRouter(tags=["misc"])


@router.get("/webp/{hex}.webp", response_class=FileResponse)
def webp_image(hex: str):
    jpg_filename = settings.static_directory / f"{hex}.jpg"
    webp_filename = settings.static_directory / f"{hex}.webp"
    if not webp_filename.exists():
        with Image.open(jpg_filename) as im:
            im.save(webp_filename, format="webp", method=6, quality=40)
    return FileResponse(webp_filename, media_type="image/webp")


@router.get("/webp/{hex}/{new_width}.webp", response_class=FileResponse)
def webp_image_new_width(hex: str, new_width: int):
    jpg_filename = settings.static_directory / f"{hex}.jpg"
    webp_filename = settings.static_directory / f"{hex}-{new_width}.webp"
    if not webp_filename.exists():
        with Image.open(jpg_filename) as im:
            width, height = im.size
            new_height = int(new_width * height / width)
            im.thumbnail((new_width, new_height))
            im.save(webp_filename, format="webp", method=6, quality=40)
    return FileResponse(webp_filename, media_type="image/webp")
