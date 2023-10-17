import cv2
import mediapipe as mp
import threading
from main import run_snake_game
import math

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def open_another_file():
    run_snake_game()

def start_game():
    global game_active
    game_active = True
    cv2.destroyWindow("Menu")
    open_another_file()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cv2.namedWindow("Menu", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Menu", 800, 600)

rectangle_x = 30
rectangle_y = 30
rectangle_width = 200
rectangle_height = 100

frame_rate = 30
game_active = False
fl = True

pointer_finger_closed = False
thumb_finger_closed = False

# Определение переменных для дополнительных прямоугольников
pink_rect = (30, 350, 200, 100)
red_rect = (400, 350, 200, 100)
blue_rect = (400, 30, 200, 100)
green_rect = (30, 30, 200, 100)  # Начальные координаты и размеры

while fl:
    if not game_active:
        cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FPS, frame_rate)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                        finger8_x = int(landmarks.landmark[8].x * frame.shape[1])
                        finger8_y = int(landmarks.landmark[8].y * frame.shape[0])
                        finger4_x = int(landmarks.landmark[4].x * frame.shape[1])
                        finger4_y = int(landmarks.landmark[4].y * frame.shape[0])

                        distance = calculate_distance((finger8_x, finger8_y), (finger4_x, finger4_y))

                        if distance < 30:
                            pointer_finger_closed = True
                        else:
                            pointer_finger_closed = False

                        if distance < 30:
                            thumb_finger_closed = True
                        else:
                            thumb_finger_closed = False

                        if pointer_finger_closed and thumb_finger_closed:
                            if rectangle_x < finger8_x < rectangle_x + rectangle_width and rectangle_y < finger8_y < rectangle_y + rectangle_height:
                                start_game()
                                fl = False
                                cv2.destroyWindow("Menu")
                                break

                            # Отслеживание нажатий на прямоугольники и отображение меток
                            if pink_rect[0] < finger8_x < pink_rect[0] + pink_rect[2] and pink_rect[1] < finger8_y < pink_rect[1] + pink_rect[3]:
                                if thumb_finger_closed:
                                    pink_rect_clicked = True
                                if pink_rect_clicked:
                                    cv2.putText(frame, "press 2", (pink_rect[0], pink_rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            if red_rect[0] < finger8_x < red_rect[0] + red_rect[2] and red_rect[1] < finger8_y < red_rect[1] + red_rect[3]:
                                if thumb_finger_closed:
                                    red_rect_clicked = True
                                if red_rect_clicked:
                                    cv2.putText(frame, "press 3", (red_rect[0], red_rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            if blue_rect[0] < finger8_x < blue_rect[0] + blue_rect[2] and blue_rect[1] < finger8_y < blue_rect[1] + blue_rect[3]:
                                if thumb_finger_closed:
                                    blue_rect_clicked = True
                                if blue_rect_clicked:
                                    cv2.putText(frame, "press 4", (blue_rect[0], blue_rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            overlay = frame.copy()
            cv2.rectangle(overlay, pink_rect[:2], (pink_rect[0] + pink_rect[2], pink_rect[1] + pink_rect[3]), (255, 105, 180), -1)
            cv2.rectangle(overlay, red_rect[:2], (red_rect[0] + red_rect[2], red_rect[1] + red_rect[3]), (0, 0, 255), -1)
            cv2.rectangle(overlay, blue_rect[:2], (blue_rect[0] + blue_rect[2], blue_rect[1] + blue_rect[3]), (255, 0, 0), -1)
            cv2.rectangle(overlay, green_rect[:2], (green_rect[0] + green_rect[2], green_rect[1] + green_rect[3]), (0, 255, 0), -1)
            cv2.addWeighted(overlay, 0.5, frame, 1 - 0.5, 0, frame)

            cv2.imshow("Menu", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
