from cv2 import Mat

from State import State
from MainMenuState import MainMenuState
from PictureTimerState import PictureTimerState
from EmailState import EmailState
from NameState import NameState
from FreeModeState import FreeModeState
from ChallengeModeState import ChallengeModeState
from RankingState import RankingState
from ControlsState import ControlsState
from FinishChallengeState import FinishChallengeState
from Hand import Hand


class StateMachine:
    def __init__(self, state: State):
        self.set_state(state)

    def set_state(self, state: State):
        self.state = state
        self.state.stateMachine = self

    def mainMenuState(self):
        return MainMenuState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
        )

    def pictureTimerState(self, next_state=None):
        return PictureTimerState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
            next_state,
        )

    def emailState(self, filename_canvas, filename_foto, next_state=None):
        return EmailState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
            filename_canvas,
            filename_foto,
            next_state,
        )

    def nameState(self, word, score, next_state=None):
        return NameState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
            word,
            score,
            next_state,
        )

    def freeModeState(self):
        self.state.imageCanvas.reset()
        return FreeModeState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            (0, 130, 1280, 720),
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
        )

    def challengeModeState(self):
        self.state.imageCanvas.reset()
        return ChallengeModeState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            (240, 140, 720, 610),
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
        )

    def rankingState(self):
        return RankingState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
        )

    def controlsState(self):
        return ControlsState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
        )

    def finishChallengeState(self, word_to_draw, limits, score):
        return FinishChallengeState(
            self.state.headerImage,
            self.state.ni_logo,
            self.state.ni_banner,
            self.state.ranking_img,
            self.state.ranking,
            self.state.video_height,
            self.state.imageCanvas,
            self.state.click_img,
            self.state.erase_img,
            self.state.paint_img,
            self.state.move_img,
            word_to_draw,
            limits,
            score,
        )

    def run(self, img, hand: Hand) -> Mat:
        state, img = self.state.run(img, hand)
        self.set_state(state)
        return img

    def handle_input(self, _input: int) -> bool:
        key_consumed, state = self.state.handle_input(_input)
        if state is not None:
            self.state(state)
        return key_consumed
