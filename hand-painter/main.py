import cv2
import time

# from predict import predict_image
import handtrackingmodule as htm #mediapipe library used in this module

from Hand import Hand
from Button import Button
from ImageCanvas import ImageCanvas
from Brush import Brush
from Ranking import Ranking
from State import State, MainMenuState

import math

NI_COLOR_RED = (54, 54, 179) #BGR

STATE = "main_menu"

cv2.namedWindow("Painter", cv2.WINDOW_AUTOSIZE)
#Importing header images using os functions
folder_location = "Utilities/Header"

ratio = 16/9
video_width = 1280
video_height = int(video_width/ratio)
headerImage = cv2.imread(f'{folder_location}/header.png')
ni_logo = cv2.imread('Utilities/logo.png')
ni_banner = cv2.imread('Utilities/banner.png', cv2.IMREAD_UNCHANGED)
ranking_img = cv2.imread('Utilities/ranking.png', cv2.IMREAD_UNCHANGED)
#ranking_img = cv2.resize(ranking_img, (100, 100))

ranking = Ranking()

#Variable to store video using cv2.VideoCapture() function
vCap = cv2.VideoCapture(0)
#Setting video resolution to 1280x720
vCap.set(3,video_width)
vCap.set(4,video_width*ratio)

#Creating an instance from the handtrackingmodule
#Setting the detection confidence to 85% for accurate performance
detector = htm.handDetector(detectionCon=0.85)

#Canvas: It'll be like an invisible screen on our video, on which drawing functions will be implemented.
#Numpy array with zeros(representing black screen) similar to the dimensions of original video frames
imageCanvas = ImageCanvas(1280, 720)

state: State = MainMenuState(
    headerImage,
    ni_logo,
    ni_banner,
    ranking_img,
    ranking,
    video_height,
    imageCanvas
)

def save_image(matrix):
    timestamp = time.time()
    filename = f'images/{timestamp}.png'
    cv2.imwrite(filename, matrix)
    return 

free_mode_btn = Button(250, 300, "MODO LIVRE") 
challenge_mode_btn = Button(700, 300, "DESAFIO")
ranking_btn = Button(500, 500, "RANKING") 
controls_btn = Button(900, 100, "CONTROLOS")
back_btn = Button(100, 250, "VOLTAR ATRAS")

hands_list: list[Hand] = []

def sqrd_distance(pos1, pos2):
    return math.dist(pos1, pos2)

def merge_hands(previous_hands: list[Hand], landmarks, fingers_up):
    new_list = []
    for idx, landmark in enumerate(landmarks):
        match = None
        best_dist = 10000
        for hand in previous_hands:
            dist = math.dist((landmark[0][1], landmark[0][2]), (hand.wrist_position[0], hand.wrist_position[1]))
            if dist > 50:
                continue
            if dist < best_dist:
                match = hand
                best_dist = dist

        if match:
            match.update_positions(landmark, fingers_up[idx])
            print("FOUND MATCH")
        else:
            match = Hand(Brush(20), landmark, fingers_up[idx])

        new_list.append(match)
    return new_list

#Displaying the video, frame by frame
while True:
    #Importing main image using read() function
    success, img = vCap.read()
    captImg = cv2.flip(img, 1)
    img = captImg #flipping the video, to compensate lateral inversion

    #Finding Hand Landmarks using handtrackingmodule
    img = detector.findHands(img, img, draw=False) 
    landmarkList = detector.findPositions(img, draw=False)
    hand_fingers = detector.fingersUp()

    hands_list = merge_hands(hands_list, landmarkList, hand_fingers)

    #Setting the header image in the main window
    #Inserting header image on the main window (Header size:1280x100)

    for hand in hands_list:
        #index finger tip coordinates(landmark number 8)
        x1,y1 = hand.index_tip_position

        #Middle finger tip coordinates(landmark number 12)
        x2,y2 = hand.middle_tip_position

        #Thumb finder tip coordinates(landmark number 4)
        x0,y0 = hand.thumb_tip_position

        #Checking which Fingers are up
        #For each finger, it returns 0 if it's up and 1 if it's not.
        #print(fingers)

        for fingers in hand_fingers:
            #Move mode: If two fingers(index and mid) are up, selection mode(no drawing)
            if hand.indicator_and_midle_up():
                #Selection mode
                cx,cy = (x1+x2)//2,(y1+y2)//2

                #color selections(In the header)
                #Whichever brush_color(region) is selected, it'll get updated in the main window
                if y1<100:
                    #Now we'll divide the whole header(1280 width) into the regions of those brushes and eraser, and change our color accordingly.
                    #Whichever region is selected, the corresponding color as well as headerImage is opted.
                    if 244<x1<330:
                        hand.brush.decrease()
                    elif 330<x1<420:
                        hand.brush.increase()
                    elif 460<x1<552:
                        hand.brush.setColor(45,45,240)
                    elif 552<x1<650:
                        hand.brush.setColor(230,78,214)
                    elif 650<x1<741:
                        hand.brush.setColor(15, 245, 245)
                    elif 741<x1<832:
                        hand.brush.setColor(13,152,35)
                    elif 832<x1<925:
                        hand.brush.setColor(250,160,15)
                    elif 962<x1<1051:
                        hand.brush.setColor(0,0,0)
                    elif 1087<x1<1175:
                        imageCanvas.reset() #clears the canvas

                #Updating the selected color
                cv2.circle(img, (cx,cy), 1, hand.brush.color, hand.brush.size)

            #Drawing mode: Index finger up
            if hand.indicator_up():
                cv2.circle(img,(x1,y1), 1, hand.brush.color, hand.brush.size + 15)
                #Drawing mode
                #Basically, we'll be drawing random lines which are actually tiny cv2.lines on loop

                #Initialising reference points
                if not hand.last_drawn:
                    hand.update_reference_points()
                
                xx, yy = hand.last_drawn

                cv2.line(imageCanvas.canvas,(xx,yy),(x1,y1),hand.brush.color, hand.brush.size)

            #Cleaning mode: All fingers up
            if hand.count_fingers_up() >= 3:
                print("cleaning mode")

            #Click mode: Thumb and Index fingers close to each other
            if hand.clicked():
                print("clicking mode")

            #Mal comportado mode: All fingers up except the middle finger
            if hand.middle_finger():
                print("mal comportado")

                #TODO: fix bug
                #img[hand[8][2]-250:hand[8][2]+250, hand[8][1]-250:hand[8][1]+250] = cv2.GaussianBlur(img[hand[8][2]-250:hand[8][2]+250, hand[8][1]-250:hand[8][1]+250], (77, 77), 77)


            #updating the reference points
            hand.update_reference_points()

    ##########################################################################################

    state, img = state.run(img, detector, captImg, landmarkList)

    cv2.imshow("Painter",img)
    key = cv2.waitKey(1)

    # Keyboard Shortcuts
    if key == ord('p'):
        predict_image(imageCanvas)
    elif key == ord('s'):
        save_image(img)
    elif key == ord('q'):
        break
    elif key == ord('+'): #remove this? or change in all hands?
        brush.increase()
    elif key == ord('-'):
        brush.decrease()

cv2.destroyAllWindows()
exit()
