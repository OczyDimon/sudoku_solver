import os
from utlis import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def recognize_img(img):
    heightImg = 450
    widthImg = 450
    model = initialize_prediction_model()  # Load the CNN Model

    # 1.Preass the image
    img = cv.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    imgThreshold = pre_process(img)

    # 2.Find all contours
    imgContours = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv.findContours(imgThreshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    cv.drawContours(imgContours, contours, -1, (0, 255, 0), 3)  # DRAW ALL DETECTED CONTOURS

    # 3.Find the biggest countour
    biggest, maxArea = biggest_contour(contours)  # Find the biggest countour

    if biggest.size != 0:
        biggest = reorder(biggest)
        cv.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25)  # Draw the biggest countour
        pts1 = np.float32(biggest)  # Prepare points for Warp
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # Preopare points for Warp
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv.warpPerspective(img, matrix, (widthImg, heightImg))
        imgWarpColored = cv.cvtColor(imgWarpColored, cv.COLOR_BGR2GRAY)

    # 4. Split the image and find digits from the image
        boxes = split_boxes(imgWarpColored)

        numbers = np.array(get_prediction(boxes, model))

        board = numbers.reshape(9, 9)

        idx = np.where(board == '0')
        board[idx] = '.'

        board = board.tolist()
        return board, True
    else:
        return [], False
