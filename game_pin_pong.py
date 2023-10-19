import subprocess
import sys

import cv2
import mediapipe as mp
import random


def run_pin_pong_game():# Инициализация MediaPipe Hands
    try:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()

        # Инициализация OpenCV
        cap = cv2.VideoCapture(0)
        width = int(cap.get(3))
        height = int(cap.get(4))

        # Параметры платформ
        paddle_height = 100
        paddle_width = 20
        left_paddle_y = height // 2 - paddle_height // 2
        right_paddle_y = height // 2 - paddle_height // 2
        paddle_speed = 10

        # Начальные параметры мяча
        ball_x = width // 2
        ball_y = height // 2
        ball_speed_x = random.choice([-8, 8])  # Случайное направление мяча
        ball_speed_y = random.choice([-8, 8])

        # Очки игроков
        left_score = 0
        right_score = 0

        # Флаги для выбора цвета разметки
        left_player_color = (0, 0, 255)  # Синий
        right_player_color = (0, 255, 0)  # Зеленый

        while True:
            ret, frame = cap.read()
            cv2.namedWindow("Ping Pong Game", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Ping Pong Game", 800, 600)

            if not ret:
                break

            # изображение горизонтально
            frame = cv2.flip(frame, 1)  # 1 означает горизонтальное отражение

            # Обработка движения рук
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame)

            # Обработчик для левой и правой руки
            left_hand_landmarks = None
            right_hand_landmarks = None

            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    # Определяем, какая рука (левая или правая)
                    if landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.5:
                        left_hand_landmarks = landmarks
                    else:
                        right_hand_landmarks = landmarks

            # Обработка движения левой руки
            if left_hand_landmarks:
                # Получение координат ключевых точек на левой руке
                x, y = int(left_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width), int(left_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

                # Управление левой платформой на основе движения указательного пальца
                left_paddle_y = y - paddle_height // 2

                # Рисуем точки руки с цветом левой платформы
                for landmark in left_hand_landmarks.landmark:
                    x_lm, y_lm = int(landmark.x * width), int(landmark.y * height)
                    frame = cv2.circle(frame, (x_lm, y_lm), 5, left_player_color, -1)

            # Обработка движения правой руки
            if right_hand_landmarks:
                # Получение координат ключевых точек на правой руке
                x, y = int(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width), int(right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

                # Управление правой платформой на основе движения указательного пальца
                right_paddle_y = y - paddle_height // 2

                # Рисуем точки руки с цветом правой платформы
                for landmark in right_hand_landmarks.landmark:
                    x_lm, y_lm = int(landmark.x * width), int(landmark.y * height)
                    frame = cv2.circle(frame, (x_lm, y_lm), 5, right_player_color, -1)

            # Обновление положения мяча
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Обработка столкновения мяча с верхней и нижней стенами
            if ball_y <= 0 or ball_y >= height:
                ball_speed_y = -ball_speed_y

            # Обработка столкновения мяча с платформами
            if (ball_x <= paddle_width and left_paddle_y <= ball_y <= left_paddle_y + paddle_height) or \
                    (ball_x >= width - paddle_width and right_paddle_y <= ball_y <= right_paddle_y + paddle_height):
                ball_speed_x = -ball_speed_x

            # Проверка, если мяч прошел мимо платформ и один из игроков забил
            if ball_x <= 0:
                right_score += 1
                ball_x = width // 2
                ball_y = height // 2
                # Установите начальную скорость после гола
                ball_speed_x = random.choice([-8, 8])
                ball_speed_y = random.choice([-8, 8])

            if ball_x >= width:
                left_score += 1
                ball_x = width // 2
                ball_y = height // 2
                # Установите начальную скорость после гола
                ball_speed_x = random.choice([-8, 8])
                ball_speed_y = random.choice([-8, 8])

            # Наложение игровых объектов на видеопоток
            frame = cv2.rectangle(frame, (0, left_paddle_y), (paddle_width, left_paddle_y + paddle_height), (0, 0, 255), -1)
            frame = cv2.rectangle(frame, (width - paddle_width, right_paddle_y), (width, right_paddle_y + paddle_height), (0, 255, 0), -1)
            frame = cv2.circle(frame, (ball_x, ball_y), 13, (252, 3, 3), -1)

            # Отображение счета
            cv2.putText(frame, f"Синий: {left_score} Зеленый: {right_score}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("Ping Pong Game", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        subprocess.run(["D:/PYTHON_/PROJECT_PYTHON_/otherPY/projDraw3D/venv/Scripts/python.exe", "menu.py"])
        sys.exit()
    except:
        print("С пин-понг чет не так")
        cap.release()
        cv2.destroyAllWindows()
        subprocess.run(["D:/PYTHON_/PROJECT_PYTHON_/otherPY/projDraw3D/venv/Scripts/python.exe", "menu.py"])
        sys.exit()
