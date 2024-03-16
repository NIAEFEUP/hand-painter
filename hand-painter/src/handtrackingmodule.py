import mediapipe as mp
from mediapipe.tasks import python
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision
import cv2
import numpy as np
import time


class handDetector:
    # Constructor, with some default values
    def __init__(
        self, mode=False, maxHands=5, detectionCon=0.5, modelComplexity=1, trackCon=0.5
    ):
        # # Assigning the hand detector as well as hand landmarks(points) detector funtions to variables of the class
        # self.mpHands = mp.solutions.hands
        # self.hands = self.mpHands.Hands(
        #     self.mode,
        #     self.maxHands,
        #     self.modelComplex,
        #     self.detectionCon,
        #     self.trackCon,
        # )
        # self.mpDraw = mp.solutions.drawing_utils

        # min_hand_detection_confidence: float = 0.5, The minimum confidence score for the hand detection to be considered successful.
        # min_hand_presence_confidence: float = 0.5, The minimum confidence score of hand presence score in the hand landmark detection.
        # min_tracking_confidence: float = 0.5, The minimum confidence score for the hand tracking to be considered successful.

        base_options = python.BaseOptions(model_asset_path="../hand_landmarker.task")
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=maxHands,
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    # function to detect hands and place/draw landmarks on them
    def findHands(self, img, draw=True):
        img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img1)

        # detector.detect -> HandLandmarkerResult(handedness=..., hand_landmarks=..., hand_world_landmarks=...)
        self.results = self.detector.detect(mp_img).hand_landmarks

        img2 = np.copy(img)

        for idx in range(len(self.results)):
            hand_landmarks = self.results[idx]

            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x, y=landmark.y, z=landmark.z
                    )
                    for landmark in hand_landmarks
                ]
            )
            solutions.drawing_utils.draw_landmarks(
                img2,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style(),
                # self.mpDraw.DrawingSpec(
                #     color=(47, 47, 255), thickness=2, circle_radius=2
                # ),  # color of points
                # self.mpDraw.DrawingSpec(
                #     color=(54, 54, 179), thickness=2, circle_radius=2
                # ),
            )  # color of connections

        self.lmList = self.findPositions(img2)
        return img2, self.lmList

    # Function to find coordinates of all the landmarks of a particular hand(default= hand number 0). Returns a list of all of them.
    def findPositions(self, img):
        self.lmList = []
        if not self.results:
            return self.lmList

        # Getting height, width and the number of channels of the original images using the .shape function
        height, width, channels = img.shape

        for myHand in self.results:
            l = []
            for id, lm in enumerate(myHand):
                # To draw those handlandmarks on the video frames
                # The coordinates recieved in lm are actually relative, i.e, 0-1. So, we need to convert them as per the size of original image.

                # Converting the relative coordinates(x,y) from lms to original coordinates(cx,cy)
                cx, cy = int(lm.x * width), int(lm.y * height)

                l.append([id, cx, cy])

            self.lmList.append(l)

        return self.lmList

    def fingersUp(self):  # checks whether the finger are up or not
        tipIDs = [4, 8, 12, 16, 20]  # Finger tip IDs
        hands = []
        for hand in self.lmList:
            fingers = []

            # thumb
            if hand[tipIDs[0]][1] < hand[tipIDs[0] - 1][1]:
                fingers.append(0)
            else:
                fingers.append(1)

            # Other fingers
            for id in range(1, 5):
                if hand[tipIDs[id]][2] > hand[tipIDs[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            hands.append(fingers)
        return hands


# Implementation/Check
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img, lmList = detector.findHands(img, img)
        print()
        print(lmList)  # list of hands with list of handmarks
        if len(lmList) != 0:
            print(lmList[0][4])  # example landmark
        # FRAME RATE
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(
            img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3
        )

        cv2.imshow("Hello", img)
        # TO TERMINATE THE PROGRAM, PRESS Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()
