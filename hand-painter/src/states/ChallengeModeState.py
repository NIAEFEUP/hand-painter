import math
from cv2 import Mat


from states.State import State
from states.PaintingState import PaintingState

from Ranking import Ranking
from ImageCanvas import ImageCanvas
from Hand import Hand
from Dataset import Dataset
from Timer import Timer
from Variables import Variables
from Text import Text


class ChallengeModeState(PaintingState):
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
            limits,
            click_img,
            erase_img,
            paint_img,
            move_img,
        )
        self.word_to_draw = Dataset().get_random_word()
        self.timer = Timer(Variables.CHALLENGE_TIME)

    def handle_input(self, _input_key: int):
        return False, self

    def run(self, img, hands: Hand) -> tuple["State", Mat]:
        square_size = 470
        top, left = 140, 240

        self.paint(img, hands)

        offsetX = left + square_size + 20
        text1 = "Desenha esta palavra"
        text2 = self.word_to_draw["name_pt"]

        img = Text.putTextCenter(img, text1, top + 50, offsetX)
        img = Text.putTextCenter(img, text2, top + 100, offsetX, color=(54, 54, 179))

        # Don't show text on 0s, where the picture is taken
        value = math.ceil(self.timer.value)
        if value != 0:
            img = Text.putTextCenter(img, "Tempo restante", top + 200, offsetX, size=70)
            img = Text.putTextCenter(img, str(value), top + 250, offsetX, size=200)

        if self.timer.completed:
            predicts = Dataset().get_predicts(self.imageCanvas.canvas)
            score = Dataset().get_compare_percentage(
                predicts, self.word_to_draw["index"]
            )
            return (
                self.stateMachine.finishChallengeState(
                    self.word_to_draw, self.limits, score
                ),
                img,
            )

        state, img = self.draw_menu(img, hands)

        for hand in hands:
            continue

        return state, img
