import cv2
import numpy as np
import cvzone

from cv2 import Mat
from states.State import State
from Hand import Hand
from Text import Text


class RankingState(State):
    def handle_input(self, _input_key: int):
        return False, self

    def run(self, img, hands: list[Hand]) -> tuple[State, Mat]:
        black_overlay = np.zeros((720, 1280, 3), np.uint8)
        img = cv2.addWeighted(img[0:720, 0:1280], 0.3, black_overlay, 0.5, 1)

        # Logo
        img = cvzone.overlayPNG(img, self.ni_banner, (20, 20))

        # Ranking image
        img = cvzone.overlayPNG(
            img, self.ranking_img, (170, self.video_height - self.ranking_img.shape[0])
        )

        # Ranking
        img = Text.drawRanking(img, self.ranking.top)

        # Button
        img = self.back_btn.draw(img, hands)

        for hand in hands:
            cv2.circle(
                img,
                (hand.index_tip_position[0], hand.index_tip_position[1]),
                1,
                self.NI_COLOR_RED,
                hand.brush.size + 15,
            )

            if self.back_btn.click(hand):
                return self.stateMachine.mainMenuState(), img

        return self, img
