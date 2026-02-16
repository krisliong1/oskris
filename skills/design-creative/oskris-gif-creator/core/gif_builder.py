#!/usr/bin/env python3
"""
GIF Builder - Core module for assembling frames into GIFs optimized for Oskris web design.

This module provides the main interface for creating GIFs from programmatically
generated frames, with automatic optimization for different use cases:
- Website animations (loading spinners, hero animations, scroll effects)
- Client demos (design showcase, before/after comparisons)
- Social media (WhatsApp, Instagram, 小红书, WeChat)
"""

from pathlib import Path
from typing import Optional

import imageio.v3 as imageio
import numpy as np
from PIL import Image


# Oskris brand colors for default styling
OSKRIS_COLORS = {
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

# Preset dimensions for different use cases
PRESETS = {
    # Website animations
    'hero': (1200, 600),
    'loading': (200, 200),
    'icon': (128, 128),
    'feature': (800, 600),
    # Social media
    'whatsapp': (640, 640),
    'instagram': (1080, 1080),
    'xiaohongshu': (1080, 1440),
    'wechat': (750, 750),
    # Client demos
    'demo': (480, 360),
    'email': (600, 400),
    'wechat_send': (240, 240),
}


class GIFBuilder:
    """Builder for creating optimized GIFs for Oskris web design projects."""

    def __init__(self, width: int = 480, height: int = 480, fps: int = 15, preset: str = None):
        """
        Initialize GIF builder.

        Args:
            width: Frame width in pixels
            height: Frame height in pixels
            fps: Frames per second
            preset: Optional preset name (overrides width/height).
                    Options: hero, loading, icon, feature, whatsapp, instagram,
                    xiaohongshu, wechat, demo, email, wechat_send
        """
        if preset and preset in PRESETS:
            self.width, self.height = PRESETS[preset]
        else:
            self.width = width
            self.height = height

        self.fps = fps
        self.preset = preset
        self.frames: list[np.ndarray] = []

    def add_frame(self, frame: np.ndarray | Image.Image):
        """
        Add a frame to the GIF.

        Args:
            frame: Frame as numpy array or PIL Image (will be converted to RGB)
        """
        if isinstance(frame, Image.Image):
            frame = np.array(frame.convert("RGB"))

        # Ensure frame is correct size
        if frame.shape[:2] != (self.height, self.width):
            pil_frame = Image.fromarray(frame)
            pil_frame = pil_frame.resize(
                (self.width, self.height), Image.Resampling.LANCZOS
            )
            frame = np.array(pil_frame)

        self.frames.append(frame)

    def add_frames(self, frames: list[np.ndarray | Image.Image]):
        """Add multiple frames at once."""
        for frame in frames:
            self.add_frame(frame)

    def optimize_colors(
        self, num_colors: int = 128, use_global_palette: bool = True
    ) -> list[np.ndarray]:
        """
        Reduce colors in all frames using quantization.

        Args:
            num_colors: Target number of colors (8-256)
            use_global_palette: Use a single palette for all frames (better compression)

        Returns:
            List of color-optimized frames
        """
        optimized = []

        if use_global_palette and len(self.frames) > 1:
            sample_size = min(5, len(self.frames))
            sample_indices = [
                int(i * len(self.frames) / sample_size) for i in range(sample_size)
            ]
            sample_frames = [self.frames[i] for i in sample_indices]

            all_pixels = np.vstack(
                [f.reshape(-1, 3) for f in sample_frames]
            )

            total_pixels = len(all_pixels)
            width = min(512, int(np.sqrt(total_pixels)))
            height = (total_pixels + width - 1) // width

            pixels_needed = width * height
            if pixels_needed > total_pixels:
                padding = np.zeros((pixels_needed - total_pixels, 3), dtype=np.uint8)
                all_pixels = np.vstack([all_pixels, padding])

            img_array = (
                all_pixels[:pixels_needed].reshape(height, width, 3).astype(np.uint8)
            )
            combined_img = Image.fromarray(img_array, mode="RGB")

            global_palette = combined_img.quantize(colors=num_colors, method=2)

            for frame in self.frames:
                pil_frame = Image.fromarray(frame)
                quantized = pil_frame.quantize(palette=global_palette, dither=1)
                optimized.append(np.array(quantized.convert("RGB")))
        else:
            for frame in self.frames:
                pil_frame = Image.fromarray(frame)
                quantized = pil_frame.quantize(colors=num_colors, method=2, dither=1)
                optimized.append(np.array(quantized.convert("RGB")))

        return optimized

    def deduplicate_frames(self, threshold: float = 0.9995) -> int:
        """
        Remove duplicate or near-duplicate consecutive frames.

        Args:
            threshold: Similarity threshold (0.0-1.0). Higher = more strict.

        Returns:
            Number of frames removed
        """
        if len(self.frames) < 2:
            return 0

        deduplicated = [self.frames[0]]
        removed_count = 0

        for i in range(1, len(self.frames)):
            prev_frame = np.array(deduplicated[-1], dtype=np.float32)
            curr_frame = np.array(self.frames[i], dtype=np.float32)

            diff = np.abs(prev_frame - curr_frame)
            similarity = 1.0 - (np.mean(diff) / 255.0)

            if similarity < threshold:
                deduplicated.append(self.frames[i])
            else:
                removed_count += 1

        self.frames = deduplicated
        return removed_count

    def save(
        self,
        output_path: str | Path,
        num_colors: int = 128,
        optimize_for: str = None,
        remove_duplicates: bool = False,
    ) -> dict:
        """
        Save frames as optimized GIF.

        Args:
            output_path: Where to save the GIF
            num_colors: Number of colors to use (fewer = smaller file)
            optimize_for: Optimization target:
                - 'loading': Ultra small (<50KB), 128x128, 48 colors
                - 'website': Small (<200KB), balanced quality
                - 'demo': Quality priority (<2MB)
                - 'social': Balanced (<5MB)
                - None: No special optimization
            remove_duplicates: If True, remove duplicate consecutive frames

        Returns:
            Dictionary with file info (path, size, dimensions, frame_count)
        """
        if not self.frames:
            raise ValueError("No frames to save. Add frames with add_frame() first.")

        output_path = Path(output_path)

        if remove_duplicates:
            removed = self.deduplicate_frames(threshold=0.9995)
            if removed > 0:
                print(f"  Removed {removed} nearly identical frames")

        # Apply optimization presets
        if optimize_for == 'loading':
            if self.width > 200 or self.height > 200:
                print(f"  Resizing from {self.width}x{self.height} to 200x200 for loading animation")
                self.width = 200
                self.height = 200
                resized = []
                for frame in self.frames:
                    pil_frame = Image.fromarray(frame)
                    pil_frame = pil_frame.resize((200, 200), Image.Resampling.LANCZOS)
                    resized.append(np.array(pil_frame))
                self.frames = resized
            num_colors = min(num_colors, 48)
            if len(self.frames) > 20:
                keep_every = max(1, len(self.frames) // 20)
                self.frames = [self.frames[i] for i in range(0, len(self.frames), keep_every)]

        elif optimize_for == 'website':
            num_colors = min(num_colors, 64)
            if len(self.frames) > 30:
                keep_every = max(1, len(self.frames) // 30)
                self.frames = [self.frames[i] for i in range(0, len(self.frames), keep_every)]

        elif optimize_for == 'demo':
            num_colors = min(num_colors, 128)

        elif optimize_for == 'social':
            num_colors = min(num_colors, 96)

        # Optimize colors with global palette
        optimized_frames = self.optimize_colors(num_colors, use_global_palette=True)

        # Calculate frame duration in milliseconds
        frame_duration = 1000 / self.fps

        # Save GIF
        imageio.imwrite(
            output_path,
            optimized_frames,
            duration=frame_duration,
            loop=0,
        )

        # Get file info
        file_size_kb = output_path.stat().st_size / 1024
        file_size_mb = file_size_kb / 1024

        info = {
            "path": str(output_path),
            "size_kb": file_size_kb,
            "size_mb": file_size_mb,
            "dimensions": f"{self.width}x{self.height}",
            "frame_count": len(optimized_frames),
            "fps": self.fps,
            "duration_seconds": len(optimized_frames) / self.fps,
            "colors": num_colors,
            "preset": self.preset,
            "optimized_for": optimize_for,
        }

        print(f"\n✓ GIF created successfully!")
        print(f"  Path: {output_path}")
        print(f"  Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
        print(f"  Dimensions: {self.width}x{self.height}")
        print(f"  Frames: {len(optimized_frames)} @ {self.fps} fps")
        print(f"  Duration: {info['duration_seconds']:.1f}s")
        print(f"  Colors: {num_colors}")

        if optimize_for:
            print(f"  Optimized for: {optimize_for}")

        # Size warnings based on use case
        target_sizes = {
            'loading': 50, 'website': 200, 'demo': 2048, 'social': 5120
        }
        if optimize_for and optimize_for in target_sizes:
            target = target_sizes[optimize_for]
            if file_size_kb > target:
                print(f"\n  ⚠️ File size ({file_size_kb:.0f}KB) exceeds target ({target}KB)")
                print("  Consider: fewer frames, smaller dimensions, or fewer colors")

        return info

    def clear(self):
        """Clear all frames (useful for creating multiple GIFs)."""
        self.frames = []
