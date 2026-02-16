#!/usr/bin/env python3
"""
Frame Composer - Utilities for composing visual elements into frames.

Provides functions for drawing shapes, text, gradients, and compositing elements
together to create animation frames for Oskris web design projects.

Includes Oskris brand color presets and web design-specific helpers like
progress bars, loading indicators, and card-style layouts.
"""

import math
from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Oskris brand colors
OSKRIS = {
    'dark': (25, 25, 25),
    'brand_blue': (37, 99, 235),
    'white': (255, 255, 255),
    'gray': (107, 114, 128),
    'light_bg': (243, 244, 246),
    'border': (229, 231, 235),
    'success': (16, 185, 129),
    'warning': (245, 158, 11),
    'error': (239, 68, 68),
}


def create_blank_frame(
    width: int, height: int, color: tuple[int, int, int] = (255, 255, 255)
) -> Image.Image:
    """
    Create a blank frame with solid color background.

    Args:
        width: Frame width
        height: Frame height
        color: RGB color tuple (default: white)

    Returns:
        PIL Image
    """
    return Image.new("RGB", (width, height), color)


def create_oskris_frame(
    width: int, height: int, style: str = "light"
) -> Image.Image:
    """
    Create a frame with Oskris brand styling.

    Args:
        width: Frame width
        height: Frame height
        style: 'light' (white bg), 'dark' (dark bg), 'blue' (brand blue bg)

    Returns:
        PIL Image with brand-styled background
    """
    colors = {
        'light': OSKRIS['white'],
        'dark': OSKRIS['dark'],
        'blue': OSKRIS['brand_blue'],
        'gray': OSKRIS['light_bg'],
    }
    bg_color = colors.get(style, OSKRIS['white'])
    return Image.new("RGB", (width, height), bg_color)


def draw_circle(
    frame: Image.Image,
    center: tuple[int, int],
    radius: int,
    fill_color: Optional[tuple[int, int, int]] = None,
    outline_color: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    Draw a circle on a frame.

    Args:
        frame: PIL Image to draw on
        center: (x, y) center position
        radius: Circle radius
        fill_color: RGB fill color (None for no fill)
        outline_color: RGB outline color (None for no outline)
        outline_width: Outline width in pixels

    Returns:
        Modified frame
    """
    draw = ImageDraw.Draw(frame)
    x, y = center
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw.ellipse(bbox, fill=fill_color, outline=outline_color, width=outline_width)
    return frame


def draw_rounded_rect(
    frame: Image.Image,
    bbox: tuple[int, int, int, int],
    radius: int = 8,
    fill_color: Optional[tuple[int, int, int]] = None,
    outline_color: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    Draw a rounded rectangle (common in modern web design).

    Args:
        frame: PIL Image to draw on
        bbox: (x1, y1, x2, y2) bounding box
        radius: Corner radius (default 8px, web standard)
        fill_color: RGB fill color
        outline_color: RGB outline color
        outline_width: Outline width

    Returns:
        Modified frame
    """
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle(
        bbox, radius=radius, fill=fill_color, outline=outline_color, width=outline_width
    )
    return frame


def draw_text(
    frame: Image.Image,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int] = (0, 0, 0),
    centered: bool = False,
) -> Image.Image:
    """
    Draw text on a frame.

    Args:
        frame: PIL Image to draw on
        text: Text to draw
        position: (x, y) position (top-left unless centered=True)
        color: RGB text color
        centered: If True, center text at position

    Returns:
        Modified frame
    """
    draw = ImageDraw.Draw(frame)
    font = ImageFont.load_default()

    if centered:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        position = (x, y)

    draw.text(position, text, fill=color, font=font)
    return frame


def create_gradient_background(
    width: int,
    height: int,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
) -> Image.Image:
    """
    Create a vertical gradient background.

    Args:
        width: Frame width
        height: Frame height
        top_color: RGB color at top
        bottom_color: RGB color at bottom

    Returns:
        PIL Image with gradient
    """
    frame = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(frame)

    r1, g1, b1 = top_color
    r2, g2, b2 = bottom_color

    for y in range(height):
        ratio = y / height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return frame


def create_radial_gradient(
    width: int,
    height: int,
    center_color: tuple[int, int, int],
    edge_color: tuple[int, int, int],
) -> Image.Image:
    """
    Create a radial gradient background (useful for spotlight/focus effects).

    Args:
        width: Frame width
        height: Frame height
        center_color: RGB color at center
        edge_color: RGB color at edges

    Returns:
        PIL Image with radial gradient
    """
    frame = Image.new("RGB", (width, height))
    pixels = frame.load()

    cx, cy = width // 2, height // 2
    max_dist = math.sqrt(cx * cx + cy * cy)

    r1, g1, b1 = center_color
    r2, g2, b2 = edge_color

    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            ratio = min(dist / max_dist, 1.0)
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            pixels[x, y] = (r, g, b)

    return frame


def draw_star(
    frame: Image.Image,
    center: tuple[int, int],
    size: int,
    fill_color: tuple[int, int, int],
    outline_color: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    Draw a 5-pointed star.

    Args:
        frame: PIL Image to draw on
        center: (x, y) center position
        size: Star size (outer radius)
        fill_color: RGB fill color
        outline_color: RGB outline color (None for no outline)
        outline_width: Outline width

    Returns:
        Modified frame
    """
    draw = ImageDraw.Draw(frame)
    x, y = center

    points = []
    for i in range(10):
        angle = (i * 36 - 90) * math.pi / 180
        radius = size if i % 2 == 0 else size * 0.4
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        points.append((px, py))

    draw.polygon(points, fill=fill_color, outline=outline_color, width=outline_width)
    return frame


def draw_progress_bar(
    frame: Image.Image,
    position: tuple[int, int],
    width: int,
    height: int = 8,
    progress: float = 0.5,
    bg_color: tuple[int, int, int] = None,
    fill_color: tuple[int, int, int] = None,
    radius: int = 4,
) -> Image.Image:
    """
    Draw a progress bar (common web UI element).

    Args:
        frame: PIL Image to draw on
        position: (x, y) top-left position
        width: Bar width
        height: Bar height (default 8px)
        progress: Fill percentage 0.0-1.0
        bg_color: Background color (default: Oskris border gray)
        fill_color: Progress fill color (default: Oskris brand blue)
        radius: Corner radius

    Returns:
        Modified frame
    """
    draw = ImageDraw.Draw(frame)
    x, y = position
    bg = bg_color or OSKRIS['border']
    fill = fill_color or OSKRIS['brand_blue']

    # Background
    draw.rounded_rectangle(
        [x, y, x + width, y + height], radius=radius, fill=bg
    )

    # Fill
    fill_width = int(width * max(0, min(1, progress)))
    if fill_width > radius * 2:
        draw.rounded_rectangle(
            [x, y, x + fill_width, y + height], radius=radius, fill=fill
        )

    return frame


def draw_loading_arc(
    frame: Image.Image,
    center: tuple[int, int],
    radius: int,
    angle: float,
    arc_length: int = 270,
    color: tuple[int, int, int] = None,
    width: int = 4,
) -> Image.Image:
    """
    Draw a loading spinner arc (common website loading animation).

    Args:
        frame: PIL Image to draw on
        center: (x, y) center position
        radius: Arc radius
        angle: Current rotation angle in degrees
        arc_length: Arc length in degrees (default 270)
        color: Arc color (default: Oskris brand blue)
        width: Arc line width

    Returns:
        Modified frame
    """
    draw = ImageDraw.Draw(frame)
    x, y = center
    c = color or OSKRIS['brand_blue']

    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw.arc(bbox, start=angle, end=angle + arc_length, fill=c, width=width)

    return frame


def draw_card(
    frame: Image.Image,
    position: tuple[int, int],
    size: tuple[int, int],
    bg_color: tuple[int, int, int] = None,
    border_color: tuple[int, int, int] = None,
    shadow: bool = True,
    radius: int = 8,
) -> Image.Image:
    """
    Draw a card-style container (common modern web design pattern).

    Args:
        frame: PIL Image to draw on
        position: (x, y) top-left position
        size: (width, height) card dimensions
        bg_color: Card background (default: white)
        border_color: Border color (default: Oskris border)
        shadow: Add subtle shadow effect
        radius: Corner radius

    Returns:
        Modified frame
    """
    draw = ImageDraw.Draw(frame)
    x, y = position
    w, h = size
    bg = bg_color or OSKRIS['white']
    border = border_color or OSKRIS['border']

    # Shadow (offset dark rectangle)
    if shadow:
        shadow_color = (200, 200, 200)
        draw.rounded_rectangle(
            [x + 2, y + 2, x + w + 2, y + h + 2],
            radius=radius, fill=shadow_color
        )

    # Card body
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=radius, fill=bg, outline=border, width=1
    )

    return frame
