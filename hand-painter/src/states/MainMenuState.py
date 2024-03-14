import cvzone
import cv2
from cv2 import Mat

from states.State import State
from Hand import Hand


class MainMenuState(State):
    def handle_input(self, _input_key: int):
        return False, self

    def run(self, img, hands: list[Hand]) -> tuple[State, Mat]:
        # Logo
        img = cvzone.overlayPNG(img, self.ni_banner, [20, 20])

        # Buttons
        img = self.free_mode_btn.draw(img, hands)
        img = self.challenge_mode_btn.draw(img, hands)
        img = self.controls_btn.draw(img, hands)
        img = self.ranking_btn.draw(img, hands)
        img = self.exit_btn.draw(img, hands)

        for hand in hands:
            cv2.circle(
                img,
                (hand.index_tip_position[0], hand.index_tip_position[1]),
                1,
                self.NI_COLOR_RED,
                hand.brush.size + 15,
            )

            if self.free_mode_btn.click(hand):
                return self.stateMachine.freeModeState(), img

            if self.challenge_mode_btn.click(hand):
                return self.stateMachine.challengeModeState(), img

            if self.ranking_btn.click(hand):
                return self.stateMachine.rankingState(), img

            if self.controls_btn.click(hand):
                return self.stateMachine.controlsState(), img

            if self.exit_btn.click(hand):
                cv2.destroyAllWindows()
                exit()

        return self, img
