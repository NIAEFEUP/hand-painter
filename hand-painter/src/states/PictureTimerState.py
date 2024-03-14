import cv2
import os
import time
import math
from cv2 import Mat

from states.State import State
from Ranking import Ranking
from ImageCanvas import ImageCanvas
from Hand import Hand
from Text import Text
from Timer import Timer
from Variables import Variables

class PictureTimerState(State):
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
        next_state=None,
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

        self.timer = Timer(Variables.SCRENNSHOT_TIME)
        self.next_state = next_state

    def handle_input(self, _input_key: int):
        return False, self

    def run(self, img, hand: Hand) -> tuple["State", Mat]:
        img = self.imageCanvas.merge(img)

        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (1280, 720), (0, 0, 0), -1)
        overlay_alpha = self.timer.overlay
        cv2.addWeighted(overlay, overlay_alpha, img, 1 - overlay_alpha, 0, img)

        # Don't show text on 0s, where the picture is taken
        value = math.ceil(self.timer.value)
        if value != 0:
            img = Text.putTextCenter(img, "Sorri!", 300, size=70)
            img = Text.putTextCenter(img, str(value), 350, size=200)

        if self.timer.completed:
            timestamp = time.time()
            os.makedirs(f"screenshots/{timestamp}")
            filename_canvas = f"screenshots/{timestamp}/desenho.png"
            filename_foto = f"screenshots/{timestamp}/foto.png"
            cv2.imwrite(filename_canvas, self.imageCanvas.white_canvas())
            cv2.imwrite(filename_foto, self.imageCanvas.merge_camera())
            return self.stateMachine.emailState(filename_canvas, filename_foto, self.next_state), img

        return self, img
