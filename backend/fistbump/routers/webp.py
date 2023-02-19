from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from PIL import Image, ImageOps
from fistbump.config import settings

router = APIRouter(tags=["misc"])

# cache webp images for a year (max limit)
headers = {"Cache-Control": "public, max-age: 31536000, smax-age: 31536000, immutable"}


@router.get("/images/{hex}.jpg", response_class=FileResponse)
async def jpg_image(hex: str):
    jpg_filename = settings.images_directory / f"{hex}.jpg"
    if not jpg_filename.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return FileResponse(jpg_filename, media_type="image/jpeg", headers=headers)


@router.get("/webp/{hex}.webp", response_class=FileResponse)
async def webp_image(hex: str):
    webp_filename = settings.images_directory / hex / "original.webp"
    if not webp_filename.exists():
        jpg_filename = settings.images_directory / hex / "original.jpg"
        with Image.open(jpg_filename) as im:
            # rotate it before save as webp don't have the exif about rotation
            im = ImageOps.exif_transpose(im)
            im.save(jpg_filename, format="jpeg", quality=50)
        with Image.open(jpg_filename) as im:
            im.save(webp_filename, format="webp", method=6, quality=40)
    return FileResponse(webp_filename, media_type="image/webp", headers=headers)


@router.get("/webp/{hex}/{new_width}.webp", response_class=FileResponse)
async def webp_image_new_width(hex: str, new_width: int):
    webp_filename = settings.images_directory / hex / f"{new_width}.webp"
    if not webp_filename.exists():
        jpg_filename = settings.images_directory / hex / "original.jpg"
        with Image.open(jpg_filename) as im:
            # rotate it before save as webp don't have the exif about rotation
            im = ImageOps.exif_transpose(im)
            width, height = im.size
            new_height = int(new_width * height / width)
            im.thumbnail((new_width, new_height))
            im.save(webp_filename, format="webp", method=6, quality=50)
    return FileResponse(webp_filename, media_type="image/webp", headers=headers)
