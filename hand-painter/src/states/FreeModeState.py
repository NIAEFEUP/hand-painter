from cv2 import Mat

from states.PaintingState import PaintingState
from states.State import State
from Hand import Hand

class FreeModeState(PaintingState):
    def run(self, img, hands: list[Hand]) -> tuple["State", Mat]:
        self.paint(img, hands)
        state, img = self.draw_menu(img, hands)
        img = self.picture_btn.draw(img, hands)

        for hand in hands:
            if self.picture_btn.click(hand):
                return self.stateMachine.pictureTimerState(), img

        return state, img
