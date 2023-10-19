import cv2
import mediapipe as mp
import threading
import math

from class_gameBar import GameBar



################################################################################################
# Импортируем функции запуска различных игр !!!! создан класс для запуска проектов, подключение не требуется
# from game_snake import run_snake_game
# from game_pin_pong import run_pin_pong_game
# from game_circle_reaction import run_circle_reaction_game
# from science_project_growth import run_science_project
################################################################################################


# Функция для вычисления расстояния между двумя точками на плоскости
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


################################################################################################
# подключен класс с запуском проектов
# Функции для запуска различных игр   !!!!!!! перенос в класс
# def start_game():
#     global game_active
#     game_active = True
#     cv2.destroyWindow("Menu")
#     run_snake_game()
#
# def start_game_2():
#     global game_active
#     game_active = True
#     cv2.destroyWindow("Menu")
#     run_pin_pong_game()
#
# def start_game_3():
#     global game_active
#     game_active = True
#     cv2.destroyWindow("Menu")
#     run_circle_reaction_game()
#
# def start_game_4():
#     global game_active
#     game_active = True
#     cv2.destroyWindow("Menu")
#     run_science_project()
################################################################################################



# Импорт модулей MediaPipe для работы с руки и отслеживания жестов
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Начальные координаты и размеры прямоугольника на экране
rectangle_x = 30
rectangle_y = 30
rectangle_width = 220
rectangle_height = 100

# Частота кадров и статус активности игры
frame_rate = 30
game_active = False
fl = True

# Флаги для отслеживания состояния пальцев
pointer_finger_closed = False
thumb_finger_closed = False

# Определение переменных для дополнительных прямоугольников
pink_rect = (30, 350, 220, 100)
red_rect = (400, 350, 220, 100)
blue_rect = (400, 30, 220, 100)
green_rect = (30, 30, 220, 100)

try:
    while fl:
        if not game_active:
            # Инициализация видеозахвата с веб-камеры
            cap = cv2.VideoCapture(0)

            while cap.isOpened():
                ret, frame = cap.read()
                cv2.namedWindow("Menu", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Menu", 800, 600)
                frame = cv2.flip(frame, 1)  # Зеркальное отражение изображения

                if not ret:
                    break

                with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(frame_rgb)

                    if results.multi_hand_landmarks:
                        for landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                            # Получаем координаты указательного и большого пальцев
                            finger8_x = int(landmarks.landmark[8].x * frame.shape[1])
                            finger8_y = int(landmarks.landmark[8].y * frame.shape[0])
                            finger4_x = int(landmarks.landmark[4].x * frame.shape[1])
                            finger4_y = int(landmarks.landmark[4].y * frame.shape[0])

                            # Вычисляем расстояние между пальцами
                            distance = calculate_distance((finger8_x, finger8_y), (finger4_x, finger4_y))

                            # Определяем, закрыты ли указательный и большой пальцы
                            if distance < 30:
                                pointer_finger_closed = True
                            else:
                                pointer_finger_closed = False

                            if distance < 30:
                                thumb_finger_closed = True
                            else:
                                thumb_finger_closed = False

                            # Отслеживание нажатий на прямоугольники и отображение меток
                            if pointer_finger_closed and thumb_finger_closed:
                                # Запуск игры "Змейка"
                                if rectangle_x < finger8_x < rectangle_x + rectangle_width and rectangle_y < finger8_y < rectangle_y + rectangle_height:
                                    GameBar.start_game_1()
                                    fl = False
                                    cv2.destroyWindow("Menu")
                                    break

                                # Запуск игры "Пин-Понг"
                                if blue_rect[0] < finger8_x < blue_rect[0] + blue_rect[2] and blue_rect[1] < finger8_y < blue_rect[1] + blue_rect[3]:
                                    cv2.putText(frame, "press 2", (blue_rect[0], blue_rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 2)
                                    GameBar.start_game_2()
                                    fl = False
                                    cv2.destroyWindow("Menu")
                                    break

                                # Запуск игры "Реакция"
                                if pink_rect[0] < finger8_x < pink_rect[0] + pink_rect[2] and pink_rect[1] < finger8_y < pink_rect[1] + pink_rect[3]:
                                    cv2.putText(frame, "press 3", (pink_rect[0], pink_rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 2)
                                    GameBar.start_game_3()
                                    fl = False
                                    cv2.destroyWindow("Menu")
                                    break

                                # Обработка действий внутри красного прямоугольника
                                if red_rect[0] < finger8_x < red_rect[0] + red_rect[2] and red_rect[1] < finger8_y < red_rect[1] + red_rect[3]:
                                    cv2.putText(frame, "press 4", (pink_rect[0], pink_rect[1] - 10),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 2)
                                    GameBar.start_game_4()
                                    fl = False
                                    cv2.destroyWindow("Menu")
                                    break
                overlay = frame.copy()

                # Отображение меток и прямоугольников для разных игр
                cv2.putText(frame, "РЕАКЦИЯ", (pink_rect[0], pink_rect[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.rectangle(overlay, pink_rect[:2], (pink_rect[0] + pink_rect[2], pink_rect[1] + pink_rect[3]), (255, 105, 180), -1)

                cv2.putText(frame, "НАУЧНЫЙ", (red_rect[0], red_rect[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.rectangle(overlay, red_rect[:2], (red_rect[0] + red_rect[2], red_rect[1] + red_rect[3]), (89, 44, 212), -1)

                cv2.putText(frame, "ПИН-ПОНГ", (blue_rect[0], blue_rect[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.rectangle(overlay, blue_rect[:2], (blue_rect[0] + blue_rect[2], blue_rect[1] + blue_rect[3]), (255, 0, 0), -1)

                cv2.putText(frame, "ЗМЕЙКА", (green_rect[0], green_rect[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.rectangle(overlay, green_rect[:2], (green_rect[0] + green_rect[2], green_rect[1] + green_rect[3]), (0, 255, 0), -1)

                cv2.addWeighted(overlay, 0.5, frame, 1 - 0.5, 0, frame)

                cv2.imshow("Menu", frame)

                # Выход из приложения при нажатии клавиши "Esc"
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            cap.release()
except:
    print("Чет не то...")
