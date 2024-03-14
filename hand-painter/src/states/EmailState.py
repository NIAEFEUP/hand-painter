import cv2
import cvzone
import threading
import string
from cv2 import Mat

from states.State import State, normal_keyboard_set, shift_keyboard_set
from Ranking import Ranking
from ImageCanvas import ImageCanvas
from TextField import TextField
from Keyboard import Keyboard, KeyboardState
from Text import Text
from Button import Button
from Hand import Hand
from Mail import Mail

class EmailState(State):
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
        filename_canvas,
        filename_foto,
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
        self.text_field = TextField()
        self.keyboard = Keyboard(lambda x: self.text_field.type(x))
        self.filename_canvas = filename_canvas
        self.filename_foto = filename_foto
        self.next_state = next_state
        self.input_handler = lambda x: self.text_field.type(x)
        self.keyboard = Keyboard(self.input_handler)

        self.submit_handler = threading.Thread(
            target=lambda: Mail().send_using_api(self.get_mail(), [self.filename_canvas, self.filename_foto])
        )

    def handle_input(self, _input_key: int):
        if _input_key == Keyboard.ENTER_KEY_CODE:
            self.submit_handler.start()
            return False, self.stateMachine.mainMenuState()
        elif _input_key == Keyboard.SHIFT_KEY_CODE:
            self.keyboard.modifier = (
                KeyboardState.NORMAL
                if self.keyboard.modifier == KeyboardState.SHIFT
                else KeyboardState.SHIFT
            )
            return True, None
        elif _input_key == Keyboard.BACKSPACE_KEY_CODE:
            self.text_field.delete()
            return True, None
        elif _input_key in (Keyboard.AT_KEY_CODE,):
            return (
                True,
                None,
            )  # special characters that should not trigger a state change
        elif (key_char := chr(_input_key)) in f'{string.ascii_lowercase}ç':
            self.input_handler(
                chr(ord(key_char) - 32)
                if self.keyboard.modifier == KeyboardState.SHIFT
                else key_char
            )
            return True, None
        elif (key_char := chr(_input_key - 32)) in f'{string.ascii_uppercase}Ç':
            self.input_handler(
                chr(ord(key_char) + 32)
                if self.keyboard.modifier == KeyboardState.SHIFT
                else key_char
            )
            return True, None

        elif (key_char := chr(_input_key)) in string.digits + "".join(
            [
                "\\",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "0",
                "'",
                "«",
                "+",
                "-",
                ".",
                ",",
                "@",
            ]
        ):
            # spaghetti

            symbol_map = {
                "\\": "|",
                "1": "!",
                "2": '"',
                "3": "#",
                "4": "$",
                "5": "%",
                "6": "&",
                "7": "/",
                "8": "(",
                "9": ")",
                "0": "=",
                "'": "?",
                "«": "»",
                "+": "*",
                "-": "_",
                ".": ":",
                ",": ";",
            }

            self.input_handler(
                symbol_map[key_char]
                if self.keyboard.modifier == KeyboardState.SHIFT and key_char != "@"
                else key_char
            )
            return True, None
        else:
            print("Unknown input key", _input_key)
            return False, self.stateMachine.mainMenuState()

    # spaghetti
    def get_mail(self):
        return self.text_field.parsed_value

    def run(self, img, hands: list[Hand]) -> tuple["State", Mat]:
        self.keyboard.draw(img, hands)

        img = Text.putText(img, "Email", (50, 70), 50, (0, 0, 0))
        text_field_ui = Button(200, 50, self.text_field.parsed_value, 800)
        img = text_field_ui.draw(img)

        if self.keyboard.modifier == KeyboardState.NORMAL:
            img = cvzone.overlayPNG(img, normal_keyboard_set, (0, 0))
        else:
            img = cvzone.overlayPNG(img, shift_keyboard_set, (0, 0))

        for hand in hands:
            cv2.circle(
                img,
                (hand.index_tip_position[0], hand.index_tip_position[1]),
                1,
                self.NI_COLOR_RED,
                hand.brush.size + 15,
            )

            kbd_mod = self.keyboard.modifier
            if self.keyboard.shift_btn.click(hand):
                self.keyboard.modifier = (
                    KeyboardState.NORMAL
                    if kbd_mod == KeyboardState.SHIFT
                    else KeyboardState.SHIFT
                )
            elif self.keyboard.delete_btn.click(hand):
                self.text_field.delete()
            elif self.keyboard.submit_btn.click(hand):
                self.submit_handler.start()
                return self.stateMachine.mainMenuState(), img

        return self, img
