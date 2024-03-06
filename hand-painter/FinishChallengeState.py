import sys
from cv2 import Mat

from State import State
from Ranking import Ranking
from ImageCanvas import ImageCanvas
from Button import Button
from Hand import Hand
from Text import Text

class FinishChallengeState(State):
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
        word_to_draw,
        limits,
        score,
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
        self.email_btn = Button(900, 350, "Enviar para email", 350, ignore_padding=True, enabled=("--no-photo" not in sys.argv))
        self.username_btn = Button(
            900,
            450,
            "Escrever nome",
            350,
            ignore_padding=True,
            enabled=self.ranking.willInsertScore(score),
        )
        self.word_to_draw = word_to_draw
        self.score = score
        self.limits = limits

    def run(self, img, hands: list[Hand]) -> tuple["State", Mat]:
        self.draw_limits(img)
        img = self.imageCanvas.merge(img)

        square_size = 350
        top, left = 100, 500

        # Right Text
        offsetX = left + square_size + 20
        word = self.word_to_draw["name_pt"]

        img = Text.putTextCenter(img, word, top + 100, offsetX, color=(54,54,179))
        img = Text.putTextCenter(img, f"{self.score}%", top + 150, offsetX, size=50)

        img = self.painting_exit_btn.draw(img, hands)
        img = self.username_btn.draw(img, hands)
        img = self.email_btn.draw(img, hands)

        for hand in hands:
            for hand in hands:
                if self.email_btn.click(hand):
                    self.email_btn.enabled = False
                    return self.stateMachine.pictureTimerState(self), img

                if self.username_btn.click(hand):
                    self.username_btn.enabled = False
                    return self.stateMachine.nameState(self.word_to_draw, self.score, self), img

                if self.painting_exit_btn.click(hand):
                    return self.stateMachine.mainMenuState(), img
            continue

        return self, img

