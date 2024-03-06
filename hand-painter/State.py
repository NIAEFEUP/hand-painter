from abc import ABC, abstractmethod
import cv2
from cv2 import Mat
import sys

from Ranking import Ranking
from ImageCanvas import ImageCanvas
from Button import Button
from Hand import Hand

folder_location = "Utilities"
normal_keyboard_set = cv2.imread(
    f"{folder_location}/normal_layout.png", cv2.IMREAD_UNCHANGED
)
shift_keyboard_set = cv2.imread(
    f"{folder_location}/shift_layout.png", cv2.IMREAD_UNCHANGED
)

class State:
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
        self._stateMachine = None

        self.free_mode_btn = Button(250, 300, "MODO LIVRE")
        self.challenge_mode_btn = Button(700, 300, "DESAFIO")
        self.ranking_btn = Button(500, 500, "RANKING")
        self.controls_btn = Button(900, 100, "CONTROLOS")
        self.back_btn = Button(100, 250, "VOLTAR ATRÁS")
        self.exit_btn = Button(900, video_height - 100, "SAIR")
        self.painting_exit_btn = Button(25, video_height - 100, "SAIR")
        self.picture_btn = Button(900, video_height - 100, "FOTO", enabled=("--no-photo" not in sys.argv))
        self.headerImage = headerImage
        self.ni_logo = ni_logo
        self.ni_banner = ni_banner
        self.ranking_img = ranking_img
        self.NI_COLOR_RED = (54, 54, 179)  # BGR NIAEFEUP color
        self.ranking = ranking
        self.video_height = video_height
        self.imageCanvas = imageCanvas
        self.click_img = click_img
        self.erase_img = erase_img
        self.paint_img = paint_img
        self.move_img = move_img

    def draw_limits(self, img):
        if self.limits is not None:
            overlay = img.copy()
            x1, y1, x2, y2 = self.limits
            x1, y1 = x1 - 1, y1 - 1
            x2, y2 = x2 + 1, y2 + 1
            cv2.rectangle(overlay, (0, 0), (x1, img.shape[0]), (0, 0, 0), -1)
            cv2.rectangle(overlay, (x2, 0), (img.shape[1], img.shape[0]), (0, 0, 0), -1)
            cv2.rectangle(overlay, (x1, 0), (x2, y1), (0, 0, 0), -1)
            cv2.rectangle(overlay, (x1, y2), (x2, img.shape[0]), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.5, img, 1 - 0.5, 0, img)

    @property
    def stateMachine(self):
        return self._stateMachine
    
    @stateMachine.setter
    def stateMachine(self, stateMachine) -> None:
        self._stateMachine = stateMachine

    @abstractmethod
    def run(self, img, hand: Hand) -> tuple["State", Mat]:
        pass

    @abstractmethod
    def handle_input(self, _input: int) -> tuple[bool, "State"]:
        pass
