"""
Color palette generation.
"""
from colorsys import hls_to_rgb
from typing import List, Sequence


def palette(ncolors: int) -> Sequence[str]:
    """
    Generate a sequence of colors. The colors should be distinct, but this
    function only does a best effort.

    Args:
        ncolors: the number of colors to generate.

    Returns:
        A sequence of color strings in hexadecimal format.
    """
    colors: List[str] = []
    hue, lightness, saturation = 0.0, 1.0, 0.5
    for i in range(ncolors):
        # Convert HLS to RGB
        r, g, b = hls_to_rgb(hue / 6, 0.4 + (lightness / 2) * 0.3, saturation)
        # Update hue and lightness
        hue = (hue + 1) % 7
        if hue == 0:
            lightness = (lightness + 1) % 3
        # Append the color in hexadecimal format
        colors.append(f"#{int(r * 256):02x}{int(g * 256):02x}{int(b * 256):02x}")
    return colors
