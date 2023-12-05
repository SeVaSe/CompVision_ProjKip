import subprocess
import sys

import cv2
import mediapipe as mp


def run_science_project():
    # Инициализация MediaPipe для обнаружения тела
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils

    # Инициализация камеры (0 - встроенная или подключенная веб-камера)
    cap = cv2.VideoCapture(1)

    # Инициализация детектора тела
    holistic = mp_holistic.Holistic()

    # Определение интересующих точек
    interesting_points = {
        0: 'Нос',
        2: 'Левый глаз',
        3: 'Левое ухо',
        5: 'Правый глаз',
        7: 'Левое ухо',
        8: 'Правое ухо',
        9: 'Рот',
        11: 'Левое плечо',
        12: 'Правое плечо',
        13: 'Левый локоть',
        14: 'Правый локоть',
        15: 'Левая кисть',
        16: 'Правая кисть',
        23: 'Левая тазовая кость',
        24: 'Правая тазовая кость',
        25: "Левое колено",
        26: "Правое колено",
        27: "Левая стопа",
        28: "Правая стопа"
    }

    # Флаг для отслеживания кулака
    is_fist = False

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            continue

        # Преобразование кадра в черно-белое изображение для ускорения обработки
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow("Full Body Detection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Full Body Detection", 800, 600)

        # Обнаружение тела на кадре
        results = holistic.process(frame)

        if results.pose_landmarks:
            # Рисуем точки тела на кадре и добавляем подписи к интересующим точкам
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                if idx in interesting_points:
                    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Красный круг
                    # Добавление подписей
                    cv2.putText(frame, interesting_points[idx], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (145, 114, 0), 2)

        # if results.left_hand_landmarks:
        #     # Определение жеста кулака на левой руке
        #     left_hand_landmarks = results.left_hand_landmarks
        #     thumb_tip = left_hand_landmarks.landmark[4]
        #     index_tip = left_hand_landmarks.landmark[8]
        #     middle_tip = left_hand_landmarks.landmark[12]
        #     ring_tip = left_hand_landmarks.landmark[16]
        #     pinky_tip = left_hand_landmarks.landmark[20]

        #     # Проверка, если все пальцы сжаты (кулак)
        #     if (
        #         thumb_tip.y > index_tip.y and
        #         index_tip.y > middle_tip.y and
        #         middle_tip.y > ring_tip.y and
        #         ring_tip.y > pinky_tip.y
        #     ):
        #         is_fist = True
        #     else:
        #         is_fist = False
        #
        # # Завершение программы, если жест кулака обнаружен
        # if is_fist:
        #     print("Пока1")
        #     cv2.destroyAllWindows()
        #     subprocess.run(["D:/PYTHON_/PROJECT_PYTHON_/otherPY/projDraw3D/venv/Scripts/python.exe", "menu.py"])
        #     sys.exit()

        cv2.imshow('Full Body Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # print("Пока2")
            # cv2.destroyAllWindows()
            # subprocess.run(["D:/PYTHON_/PROJECT_PYTHON_/otherPY/projDraw3D/venv/Scripts/python.exe", "menu.py"])
            # sys.exit()

    cap.release()
    cv2.destroyAllWindows()
    print("Пока3")
    subprocess.run(
        ["C:/PYTHON_/_PROJECT_PYTHON/Python_Project_Other/CompVision_ProjKip/venv/Scripts/python.exe", "menu.py"])
    sys.exit()
