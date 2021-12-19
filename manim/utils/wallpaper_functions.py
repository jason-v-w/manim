"""A selection of common functions for how to create a wallpaper from an image.

Each wallpaper function accepts two images (a background and a foreground) and returns a new image with the same dimensions as the background. Each places the foreground onto the background in a certain way. Neither of the input images are modified.
"""


__all__ = [
    "wallpaper_scale",
    "wallpaper_shift",
    "wallpaper_stretch",
    "wallpaper_tile",
]

import numpy as np
import PIL


def _manim_coords_to_PIL_coords(image: PIL.Image, coords: np.ndarray) -> np.array:
    """Convert Manim style coordinates to pixel coordinates within an image.

    The basic Manim coordinates are converted as follows:

    - UR, UL, DR, DL are converted to the pixel indices of the respective corners of the image
    - UP, DOWN, RIGHT, LEFT are converted to the pixel indices of the centers of the
         respective edges of the image
    - ORIGIN is converted to the pixel indices of the center of the image

    Parameters
    ----------
    image
        The image to find coordinates with respect to.

    coords
        The manim style coordinates to convert.

    Returns
    -------
    class:`np.array`
        A 2 element array with the integer pixel coordinates (PIL style)
    """
    # in Manim, +y is up, but in PIL, +y is down. Also only x and y are needed coords =
    np.array([coords[0], -coords[1]])

    # coords scale is -1 to 1, and percentage_coords scale is 0 to 1 and this is linear
    # interpolation between them
    percentage_coords = (coords + 1) / 2

    # subtract one from each coordinate of the size to give the max pixel value when
    # 0-indexed
    max_coords = [n - 1 for n in np.array(image.size)]
    return np.round(percentage_coords * max_coords).astype(int)


def wallpaper_stretch(background: PIL.Image, image: PIL.Image) -> PIL.Image:
    """Stretch image to completely cover background."""
    return image.copy().resize(background.size)


def wallpaper_scale(background: PIL.Image, image: PIL.Image):
    """Scale image up or down to completely cover background in at least one dimension."""
    bgd_sz = np.array(background.size)
    img_sz = np.array(image.size)

    ratio = np.min(bgd_sz / img_sz)  # a single float

    # TODO: the math is correct, but rounding errors might be introduced; some
    # additional logic could be added to ensure that one of the dimensions of the image
    # is maxed out
    return Center(
        background, image.copy().resize(tuple(np.round(img_sz * ratio).astype(int)))
    )


def _wallpaper_tile_shift_helper(
    background: PIL.Image,
    image: PIL.Image,
    tile: bool,
    background_position: np.array = ORIGIN,
    image_position: np.array = ORIGIN,
) -> PIL.Image:
    bgd_sz = np.array(background.size)
    img_sz = np.array(image.size)
    bgd_pos = _manim_coords_to_PIL_coords(background, background_position)
    img_pos = _manim_coords_to_PIL_coords(image, image_position)

    # coordinates (in background) of the upper left corner of the image rather than
    # coordinates of image_position relative to background
    true_img_pos = bgd_pos - img_pos

    result = background.copy()
    if not tile:
        result.paste(image, box=tuple(true_img_pos))
        return result

    # modular arithmetic to find the position of the first (most upper left) image in
    # the tiling in the second step, non-zero coordinate positions must become negative
    # pasting image at base_img_pos will guarantee that some pixels are on the
    # background
    base_img_pos = np.remainder(true_img_pos, img_sz)
    base_img_pos = [0 if n == 0 else n - s for n, s in zip(base_img_pos, img_sz)]

    x_times, y_times = np.ceil(bgd_sz / img_sz).astype(int) + np.array([1, 1])

    for i in range(x_times):
        for j in range(y_times):
            result.paste(image, box=tuple(base_img_pos + img_sz * [i, j]))
    return result


def wallpaper_shift(
    background: PIL.Image,
    image: PIL.Image,
    background_position: np.array = ORIGIN,
    image_position: np.array = ORIGIN,
):
    """Shift image so `image_position` is located at `background_position`."""
    return _wallpaper_tile_shift_helper(
        background, image, False, background_position, image_position
    )


def wallpaper_tile(
    background: PIL.Image,
    image: PIL.Image,
    background_position: np.array = ORIGIN,
    image_position: np.array = ORIGIN,
):
    """Shift image so `image_position` is located at `background_position` and tessellate."""
    return _wallpaper_tile_shift_helper(
        background, image, True, background_position, image_position
    )
