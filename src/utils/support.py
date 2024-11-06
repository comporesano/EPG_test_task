from fastapi import Form

from pydantic import Field

from PIL import Image, ImageDraw, ImageFont

from inspect import signature, Parameter

from .constants import EARTH_RADIUS

from functools import lru_cache

from timeit import timeit

import io
import math


def form_body(cls):
    sig = signature(cls)
    new_params = []

    for name, param in sig.parameters.items():
        if param.annotation is Field:
            default_value = param.default if param.default is not Field else ...
            new_param = Parameter(
                name=name,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Form(default_value),
                annotation=param.annotation
            )
            new_params.append(new_param)
        else:
            new_params.append(param)

    new_sig = sig.replace(parameters=new_params)
    cls.__signature__ = new_sig
    
    return cls


async def watermark_put(original_img,
                        watermark_text: str, 
                        color: tuple,
                        font_path: str,
                        font_size: int,
                        wm_pos: tuple):
    image = Image.open(io.BytesIO(original_img)).convert("RGBA")
    drawable = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    drawable.text(wm_pos, watermark_text, fill=color, font=font)
    
    wmarked_arr = io.BytesIO()
    image.save(wmarked_arr, format="PNG")
    wmarked_arr.seek(0)
    
    return wmarked_arr.read()


@lru_cache
def haversine(point1: tuple[float] = None, 
              point2: tuple[float] = None
) -> float:
    x1, y1 = point1
    x2, y2 = point2
    x1_rad = math.radians(x1)
    y1_rad = math.radians(y1)
    x2_rad = math.radians(x2)
    y2_rad = math.radians(y2)
    
    delta_lat = x2_rad - x1_rad
    delta_long = y2_rad - y1_rad
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(x1_rad) * math.cos(x2_rad) * math.sin(delta_long / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return EARTH_RADIUS * c    
