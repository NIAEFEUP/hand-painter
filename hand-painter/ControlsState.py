import numpy as np
import cv2
import cvzone

from State import State
from Ranking import Ranking
from ImageCanvas import ImageCanvas
from Hand import Hand
from Text import Text
from Brush import BigEraser, SmallEraser

class ControlsState(State):
    def handle_input(self, _input_key: int):
        return False, self

    def __init__(
        self,
        headerImage,
        ni_logo,
        ni_banner,
        ranking_img,
        ranking: Ranking,
        video_height,
        imageCanvas: ImageCanvas,
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

    def run(self, img, hands: list[Hand]):
        black_overlay = np.zeros((720, 1280, 3), np.uint8)
        img = cv2.addWeighted(img[0:720, 0:1280], 0.3, black_overlay, 0.5, 1)

        # Controls
        x, y, h = 650, 150, 48

        img = Text.putText(img, "Controls", (x, y - 2 * h))

        icon_width, icon_height = 70, 70
        icon_size = (icon_width, icon_height)

        # TODO: add interactive controls
        # a success indications should be shown when doing the right movement on top of each control display

        for i, item in enumerate(
            [
                (
                    self.click_img,
                    "Aperta os dedos para clickar na\nárea do ecrã debaixo deles",
                ),
                (self.paint_img, "Levanta o indicador para\npintares no ecrã"),
                (
                    self.move_img,
                    "Levanta o indicador e o dedo do\nmeio para mover o pincel sem pintar",
                ),
                (self.erase_img, "Levanta 3/4 dedos para\napagares partes do desenho"),
            ]
        ):
            icon, description = item

            # spaghetti

            img = cvzone.overlayPNG(
                img,
                cv2.resize(icon, icon_size, interpolation=cv2.INTER_AREA),
                (x, 150 + icon_height * 2 * i),
            )

            img = Text.putText(
                img, description, (x + icon_width + 15, 155 + icon_height * 2 * i), 30
            )

        # Button
        img = self.back_btn.draw(img, hands)

        for hand in hands:
            x1, y1 = hand.index_tip_position
            x2, y2 = hand.middle_tip_position

            if hand.indicator_and_middle_up():
                x, y = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x, y), 1, self.NI_COLOR_RED, 20)

            elif hand.indicator_up():
                cv2.circle(img, (x1, y1), 1, self.NI_COLOR_RED, 35)

                if not hand.last_drawn:
                    hand.update_reference_points()

            elif 3 <= (hand_count_up := hand.count_fingers_up()) <= 4:
                eraser = SmallEraser() if hand_count_up == 3 else BigEraser()

                if not hand.last_drawn:
                    hand.update_reference_points()

                cv2.circle(img, (x2, y2), eraser.size, self.NI_COLOR_RED)

            hand.update_reference_points()

            if self.back_btn.click(hand):
                return self.stateMachine.mainMenuState(), img

        return self, img
