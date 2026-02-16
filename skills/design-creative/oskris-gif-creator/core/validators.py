#!/usr/bin/env python3
"""
Validators - Check if GIFs meet requirements for different Oskris use cases.

Validates GIFs against size and dimension constraints for:
- Website animations (loading, hero, features)
- Social media (WhatsApp, Instagram, 小红书, WeChat)
- Client demos and presentations
- Email embeds
"""

from pathlib import Path


# Target specifications for each use case
USE_CASE_SPECS = {
    'loading': {
        'max_size_kb': 50,
        'dimensions': (200, 200),
        'max_frames': 20,
        'description': 'Website loading animation',
    },
    'icon': {
        'max_size_kb': 30,
        'dimensions': (128, 128),
        'max_frames': 12,
        'description': 'Animated icon/favicon',
    },
    'hero': {
        'max_size_kb': 2048,
        'dimensions': (1200, 600),
        'max_frames': 60,
        'description': 'Website hero section animation',
    },
    'feature': {
        'max_size_kb': 1024,
        'dimensions': (800, 600),
        'max_frames': 45,
        'description': 'Feature showcase animation',
    },
    'demo': {
        'max_size_kb': 2048,
        'dimensions': (480, 360),
        'max_frames': 90,
        'description': 'Client demo / design preview',
    },
    'email': {
        'max_size_kb': 1024,
        'dimensions': (600, 400),
        'max_frames': 30,
        'description': 'Email-embedded animation',
    },
    'whatsapp': {
        'max_size_kb': 5120,
        'dimensions': (640, 640),
        'max_frames': 60,
        'description': 'WhatsApp status/sticker',
    },
    'instagram': {
        'max_size_kb': 5120,
        'dimensions': (1080, 1080),
        'max_frames': 60,
        'description': 'Instagram post animation',
    },
    'xiaohongshu': {
        'max_size_kb': 5120,
        'dimensions': (1080, 1440),
        'max_frames': 60,
        'description': '小红书 post animation',
    },
    'wechat': {
        'max_size_kb': 5120,
        'dimensions': (750, 750),
        'max_frames': 60,
        'description': 'WeChat moments animation',
    },
    'wechat_send': {
        'max_size_kb': 500,
        'dimensions': (240, 240),
        'max_frames': 20,
        'description': 'WeChat chat GIF (small)',
    },
}


def validate_gif(
    gif_path: str | Path, use_case: str = "demo", verbose: bool = True
) -> tuple[bool, dict]:
    """
    Validate GIF for a specific Oskris use case.

    Args:
        gif_path: Path to GIF file
        use_case: Target use case. Options:
            - Website: 'loading', 'icon', 'hero', 'feature'
            - Demo: 'demo', 'email'
            - Social: 'whatsapp', 'instagram', 'xiaohongshu', 'wechat', 'wechat_send'
        verbose: Print validation details

    Returns:
        Tuple of (passes: bool, results: dict with all details)
    """
    from PIL import Image

    gif_path = Path(gif_path)

    if not gif_path.exists():
        return False, {"error": f"File not found: {gif_path}"}

    spec = USE_CASE_SPECS.get(use_case)
    if not spec:
        return False, {"error": f"Unknown use case: {use_case}. Options: {list(USE_CASE_SPECS.keys())}"}

    # Get file size
    size_bytes = gif_path.stat().st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    # Get dimensions and frame info
    try:
        with Image.open(gif_path) as img:
            width, height = img.size

            frame_count = 0
            try:
                while True:
                    img.seek(frame_count)
                    frame_count += 1
            except EOFError:
                pass

            try:
                duration_ms = img.info.get("duration", 100)
                total_duration = (duration_ms * frame_count) / 1000
                fps = frame_count / total_duration if total_duration > 0 else 0
            except Exception:
                total_duration = None
                fps = None

    except Exception as e:
        return False, {"error": f"Failed to read GIF: {e}"}

    # Validate against spec
    target_w, target_h = spec['dimensions']
    size_ok = size_kb <= spec['max_size_kb']
    dim_ok = (width == target_w and height == target_h)
    dim_acceptable = (
        abs(width - target_w) <= target_w * 0.2 and
        abs(height - target_h) <= target_h * 0.2
    )
    frames_ok = frame_count <= spec['max_frames']

    all_pass = size_ok and (dim_ok or dim_acceptable) and frames_ok

    results = {
        "file": str(gif_path),
        "use_case": use_case,
        "description": spec['description'],
        "passes": all_pass,
        "width": width,
        "height": height,
        "target_dimensions": f"{target_w}x{target_h}",
        "size_kb": size_kb,
        "size_mb": size_mb,
        "max_size_kb": spec['max_size_kb'],
        "frame_count": frame_count,
        "max_frames": spec['max_frames'],
        "duration_seconds": total_duration,
        "fps": fps,
        "checks": {
            "size": "✅" if size_ok else "❌",
            "dimensions": "✅" if dim_ok else ("⚠️" if dim_acceptable else "❌"),
            "frames": "✅" if frames_ok else "❌",
        },
    }

    if verbose:
        status = "✅ PASS" if all_pass else "❌ FAIL"
        print(f"\n{status} - Validating for: {spec['description']} ({use_case})")
        print(f"  Dimensions: {width}x{height} (target: {target_w}x{target_h}) {results['checks']['dimensions']}")
        print(f"  File size: {size_kb:.1f} KB (max: {spec['max_size_kb']} KB) {results['checks']['size']}")
        print(f"  Frames: {frame_count} (max: {spec['max_frames']}) {results['checks']['frames']}")
        if fps:
            print(f"  FPS: {fps:.1f}, Duration: {total_duration:.1f}s")

        if not all_pass:
            print(f"\n  Suggestions:")
            if not size_ok:
                print(f"    - Reduce file size: fewer colors, fewer frames, or smaller dimensions")
            if not dim_ok and not dim_acceptable:
                print(f"    - Resize to {target_w}x{target_h}")
            if not frames_ok:
                print(f"    - Reduce to {spec['max_frames']} frames or fewer")

    return all_pass, results


def is_ready(
    gif_path: str | Path, use_case: str = "demo", verbose: bool = True
) -> bool:
    """
    Quick check if GIF is ready for the specified use case.

    Args:
        gif_path: Path to GIF file
        use_case: Target use case (see validate_gif for options)
        verbose: Print feedback

    Returns:
        True if GIF meets all requirements
    """
    passes, _ = validate_gif(gif_path, use_case, verbose)
    return passes


def validate_all(gif_path: str | Path) -> dict:
    """
    Validate GIF against ALL use cases and show which ones it's ready for.

    Args:
        gif_path: Path to GIF file

    Returns:
        Dictionary of {use_case: passes} for all use cases
    """
    print(f"\nValidating {gif_path} against all Oskris use cases:")
    print("=" * 60)

    results = {}
    for use_case in USE_CASE_SPECS:
        passes, _ = validate_gif(gif_path, use_case, verbose=False)
        spec = USE_CASE_SPECS[use_case]
        status = "✅" if passes else "❌"
        print(f"  {status} {use_case:15s} - {spec['description']}")
        results[use_case] = passes

    passed = sum(1 for v in results.values() if v)
    print(f"\nReady for {passed}/{len(results)} use cases")

    return results
