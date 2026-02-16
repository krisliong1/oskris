"""
Oskris GIF Creator - Core utilities for creating professional animations.

Modules:
    gif_builder: Main GIF assembly and optimization
    easing: Timing/easing functions for smooth animations
    frame_composer: Drawing helpers and frame composition
    validators: Validation against different use case requirements
"""

from .gif_builder import GIFBuilder, OSKRIS_COLORS, PRESETS
from .easing import interpolate, get_easing, EASING_FUNCTIONS
from .frame_composer import (
    create_blank_frame,
    create_oskris_frame,
    create_gradient_background,
    create_radial_gradient,
    draw_circle,
    draw_rounded_rect,
    draw_text,
    draw_star,
    draw_progress_bar,
    draw_loading_arc,
    draw_card,
    OSKRIS,
)
from .validators import validate_gif, is_ready, validate_all

__all__ = [
    'GIFBuilder', 'OSKRIS_COLORS', 'PRESETS',
    'interpolate', 'get_easing',
    'create_blank_frame', 'create_oskris_frame',
    'create_gradient_background', 'create_radial_gradient',
    'draw_circle', 'draw_rounded_rect', 'draw_text', 'draw_star',
    'draw_progress_bar', 'draw_loading_arc', 'draw_card',
    'validate_gif', 'is_ready', 'validate_all',
]
