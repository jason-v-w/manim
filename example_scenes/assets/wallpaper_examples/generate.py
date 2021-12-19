"""An example file used to generate example images for wallpaper examples.

This is the source file for the images used in the wallpaper examples. Each image
includes a circle to demonstrate distortions that might be introduced by some wallpaper
functions. Each image also includes its own pixel resolution so that scaling effects of
the image can be seen.
"""

from manim import *


class BaseImg(Scene):
    def __init__(self, width=1920, height=1080, color=GRAY):
        config.pixel_width = width
        config.pixel_height = height
        config.frame_width = config.pixel_width
        config.frame_height = config.pixel_height
        self.color = color
        super().__init__()

    def construct(self):
        size = min(config.pixel_width, config.pixel_height)
        text_scale = size / 4
        r = size / 2.5
        s = size * 3

        self.camera.background_color = self.color
        self.add(Circle(radius=r, color=BLACK, stroke_width=s))
        self.add(
            Rectangle(
                width=config.frame_width - size * 0.2,
                height=config.frame_height - size * 0.2,
                color=BLACK,
                stroke_width=s,
            )
        )
        self.add(
            MathTex(f"{config.pixel_width}\\times{config.pixel_height}")
            .scale(text_scale)
            .move_to(ORIGIN)
            .set_color(BLACK)
        )


class SquareSmall(BaseImg):
    def __init__(self):
        super().__init__(512, 512, BLUE)


class SquareBig(BaseImg):
    def __init__(self):
        super().__init__(3000, 3000, TEAL)


class RectHorizSmall(BaseImg):
    def __init__(self):
        super().__init__(512, 256, GREEN)


class RectHorizBig(BaseImg):
    def __init__(self):
        super().__init__(3000, 1500, YELLOW)


class RectVertSmall(BaseImg):
    def __init__(self):
        super().__init__(256, 512, GOLD)


class RectVertBig(BaseImg):
    def __init__(self):
        super().__init__(1500, 3000, ORANGE)


class FrameSmall(BaseImg):
    def __init__(self):
        super().__init__(480, 270, WHITE)


class FramePerfect(BaseImg):
    def __init__(self):
        super().__init__(1920, 1080, MAROON)


class FrameBig(BaseImg):
    def __init__(self):
        super().__init__(3840, 2160, PURPLE)
