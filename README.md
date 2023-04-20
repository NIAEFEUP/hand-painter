## Folder Structure
### hand-painter
Contains the code to run the application.
The application uses the [MediaPipe](https://google.github.io/mediapipe/) library to track the hand and the [OpenCV](https://opencv.org/) library to draw on the screen.
There are two modes:
- `paint` mode: the user(s) can draw on the screen using the hand(s).
- `challenge` mode: the user is challenged to draw the object of a random word using the hand and the application will find the similarity between the drawing and the chosen word.

To **set up** the application, read the [README](hand-painter/README.md) file in the `hand-painter` folder.

### cnn (Conventual Neural Network)
Contains the code to train the CNN model.
The model is used to predict the class of a drawing.
It's trained on the dataset provided by the [QuickDraw](https://quickdraw.withgoogle.com/data) project.

