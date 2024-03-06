import cv2
from cv2 import Mat
import numpy as np
import cvzone
from abc import abstractmethod

from State import State
from Ranking import Ranking
from ImageCanvas import ImageCanvas
from typing import ClassVar
from Brush import Brush, BigEraser, SmallEraser
from Hand import Hand

class PaintingState(State):
    def __init__(
        self,
        headerImage,
        ni_logo,
        ni_banner,
        ranking_img,
        ranking: Ranking,
        video_height,
        imageCanvas: ImageCanvas,
        limits,
        click_img,
        erase_img,
        paint_img,
        move_img,
    ) -> None:
        super().__init__(
            headerImage,
            ni_logo,
            ni_banner,
            ranking_img,
            ranking,
            video_height,
            imageCanvas,
            click_img,
            erase_img,
            paint_img,
            move_img,
        )
        self.limits = limits  # tuple[int, int, int, int]

    RED_BRUSH: ClassVar[Brush] = Brush(20, (45, 45, 240))
    PINK_BRUSH: ClassVar[Brush] = Brush(20, (230, 78, 214))
    YELLOW_BRUSH: ClassVar[Brush] = Brush(20, (15, 245, 245))
    GREEN_BRUSH: ClassVar[Brush] = Brush(20, (13, 152, 35))
    BLUE_BRUSH: ClassVar[Brush] = Brush(20, (250, 160, 15))

    def handle_input(self, _input_key: int):
        return False, self

    def paint(self, img, hands):
        self.draw_limits(img)

        # Add limits parameter for square limits in challenge mode
        for hand in hands:
            # index finger tip coordinates(landmark number 8)
            x1, y1 = hand.index_tip_position

            # Middle finger tip coordinates(landmark number 12)
            x2, y2 = hand.middle_tip_position

            # Checking which Fingers are up
            # For each finger, it returns 0 if it's up and 1 if it's not.
            # print(fingers)

            x, y = 0, 0

            if hand.indicator_and_middle_up():
                # Selection mode
                x, y = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x, y), 1, hand.brush.color, hand.brush.size)

                # color selections(In the header)
                # Whichever brush_color(region) is selected, it'll get updated in the main window
                if y1 < 100:
                    # Now we'll divide the whole header(1280 width) into the regions of those brushes and eraser, and change our color accordingly.
                    # Whichever region is selected, the corresponding color as well as headerImage is opted.
                    if 244 < x1 < 330:
                        hand.brush.decrease()
                    elif 330 < x1 < 420:
                        hand.brush.increase()
                    elif 460 < x1 < 552:
                        hand.set_brush(PaintingState.RED_BRUSH)
                    elif 552 < x1 < 650:
                        hand.set_brush(PaintingState.PINK_BRUSH)
                    elif 650 < x1 < 741:
                        hand.set_brush(PaintingState.YELLOW_BRUSH)
                    elif 741 < x1 < 832:
                        hand.set_brush(PaintingState.GREEN_BRUSH)
                    elif 832 < x1 < 925:
                        hand.set_brush(PaintingState.BLUE_BRUSH)
                    elif 1122 < x1 < 1211:
                        self.imageCanvas.reset()  # clears the canvas

            # Drawing mode: Index finger up
            elif hand.indicator_up():
                cv2.circle(img, (x1, y1), 1, hand.brush.color, hand.brush.size + 15)

                # Drawing mode

                # Initialising reference points
                if not hand.last_drawn:
                    hand.update_reference_points()

                x, y = hand.last_drawn

                cv2.line(
                    self.imageCanvas.canvas,
                    (x, y),
                    (x1, y1),
                    hand.brush.color,
                    hand.brush.size,
                )

                # Create a mask with the limiits
                mask = np.zeros_like(self.imageCanvas.canvas)
                mask = cv2.rectangle(
                    mask,
                    (self.limits[0], self.limits[1]),
                    (self.limits[2], self.limits[3]),
                    (255, 255, 255),
                    -1,
                )
                self.imageCanvas.canvas = cv2.bitwise_and(self.imageCanvas.canvas, mask)

            elif 3 <= (hand_count_up := hand.count_fingers_up()) <= 4:
                eraser = SmallEraser() if hand_count_up == 3 else BigEraser()

                if not hand.last_drawn:
                    hand.update_reference_points()

                x, y = hand.last_drawn

                cv2.circle(img, (x2, y2), eraser.size, eraser.color)
                cv2.circle(
                    self.imageCanvas.canvas,
                    (x2, y2),
                    eraser.size,
                    eraser.color,
                    -1,  # any negative value should suffice
                )

            # Updating the selected color
            # cv2.circle(img, (x, y), 1, hand.brush.color, hand.brush.size + hand.indicator_up()*15)
            hand.update_reference_points()

    def draw_menu(self, img, hands):
        img = cvzone.overlayPNG(img, self.headerImage, (0, 20))

        # Merge Video capture and Canvas
        img = self.imageCanvas.merge(img)

        # Logo
        img = cvzone.overlayPNG(img, self.ni_logo, (20, 20))

        img = self.painting_exit_btn.draw(img, hands)

        # TODO CHANGE THIS TO ABOVE UI?
        for hand in hands:
            if self.painting_exit_btn.click(hand):
                return self.stateMachine.mainMenuState(), img

        return self, img

    @abstractmethod
    def run(self, img, hands: Hand) -> tuple["State", Mat]:
        pass
