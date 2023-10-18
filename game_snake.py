import cv2
import mediapipe as mp
import pygame
import random
import subprocess


# Инициализация Pygame
def run_snake_game():
    pygame.init()

    # Параметры игры
    screen_width = 640
    screen_height = 480
    cell_size = 20
    fruit_size = 40
    snake_speed = 10

    # Цвета
    white = (255, 255, 255)
    dark_sea = (0, 51, 102)  # Цвет головы змеи (темно-морской)
    blue = (0, 0, 255)       # Цвет тела змеи (голубой)

    # Инициализация экрана Pygame
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Змейка')

    # Инициализация змейки
    snake = [(screen_width // 2, screen_height // 2)]
    snake_direction = (0, -1)

    # Инициализация фрукта
    fruit = (random.randint(0, (screen_width - fruit_size) // cell_size) * cell_size,
             random.randint(0, (screen_height - fruit_size) // cell_size) * cell_size)

    # Инициализация OpenCV и Mediapipe
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Инициализация захвата видео

    cap = cv2.VideoCapture(0)  # 111111111111111111111111111111111111111111

    hand_x = 0
    hand_y = 0
    prev_hand_x = 0
    prev_hand_y = 0

    # Сглаживание движения указательного пальца
    smooth_factor = 0.8
    smoothed_vector_x = 0
    smoothed_vector_y = 0

    # Минимальная скорость для изменения направления
    min_speed_threshold = 5

    # Инициализация времени
    clock = pygame.time.Clock()

    game_over = False

    # Инициализация счетчиков
    apple_count = 0
    game_start_time = pygame.time.get_ticks()

    # Шрифт для отображения счетчиков
    font = pygame.font.Font(None, 36)

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while not game_over:
            ret, image = cap.read()
            if not ret:
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            if results.multi_hand_landmarks:
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                for landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
                    wrist_x = int(landmarks.landmark[mp_hands.HandLandmark.WRIST].x * screen_width)
                    wrist_y = int(landmarks.landmark[mp_hands.HandLandmark.WRIST].y * screen_height)
                    cv2.circle(image, (wrist_x, wrist_y), 8, (0, 255, 0), -1)

                    prev_hand_x, prev_hand_y = hand_x, hand_y
                    hand_x, hand_y = wrist_x, wrist_y

                    vector_x = hand_x - prev_hand_x
                    vector_y = hand_y - prev_hand_y

                    smoothed_vector_x = (1 - smooth_factor) * vector_x + smooth_factor * smoothed_vector_x
                    smoothed_vector_y = (1 - smooth_factor) * vector_y + smooth_factor * smoothed_vector_y

                    if abs(smoothed_vector_x) > min_speed_threshold or abs(smoothed_vector_y) > min_speed_threshold:
                        if abs(smoothed_vector_x) > abs(smoothed_vector_y):
                            if smoothed_vector_x < 0 and snake_direction != (1, 0):
                                snake_direction = (-1, 0)
                            elif smoothed_vector_x > 0 and snake_direction != (-1, 0):
                                snake_direction = (1, 0)
                        else:
                            if smoothed_vector_y < 0 and snake_direction != (0, 1):
                                snake_direction = (0, -1)
                            elif smoothed_vector_y > 0 and snake_direction != (0, -1):
                                snake_direction = (0, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            if not game_over:
                # Обновление змейки
                snake_head = (snake[0][0] + snake_direction[0] * cell_size, snake[0][1] + snake_direction[1] * cell_size)

                # Проверка, чтобы змейка не ушла за пределы экрана
                if snake_head[0] < 0:
                    snake_head = (screen_width - cell_size, snake_head[1])
                elif snake_head[0] >= screen_width:
                    snake_head = (0, snake_head[1])
                if snake_head[1] < 0:
                    snake_head = (snake_head[0], screen_height - cell_size)
                elif snake_head[1] >= screen_height:
                    snake_head = (snake_head[0], 0)

                snake.insert(0, snake_head)

                # Проверка на столкновение с фруктом
                if (snake_head[0] <= fruit[0] + fruit_size and
                        snake_head[0] + cell_size >= fruit[0] and
                        snake_head[1] <= fruit[1] + fruit_size and
                        snake_head[1] + cell_size >= fruit[1]):
                    # Змейка съела фрукт, увеличиваем ее длину
                    while True:
                        fruit = (random.randint(0, (screen_width - fruit_size) // cell_size) * cell_size,
                                 random.randint(0, (screen_height - fruit_size) // cell_size) * cell_size)
                        if fruit not in snake:
                            break

                    # Увеличение счетчика яблок
                    apple_count += 1

                else:
                    snake.pop()

                # Проверка на столкновение головы с телом
                if snake_head in snake[1:]:
                    game_over = True

                # Рендеринг экрана Pygame
                screen.fill(white)
                for i, segment in enumerate(snake):
                    color = dark_sea if i == 0 else blue
                    pygame.draw.rect(screen, color, (segment[0], segment[1], cell_size, cell_size))
                pygame.draw.rect(screen, (168, 50, 50), (fruit[0], fruit[1], fruit_size, fruit_size))

                # Отображение счетчика яблок
                apple_text = font.render(f'Яблок: {apple_count}', True, (0, 0, 0))
                screen.blit(apple_text, (10, 10))

                # Отображение счетчика времени
                elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000
                time_text = font.render(f'Время: {elapsed_time} секунд', True, (0, 0, 0))
                screen.blit(time_text, (10, 50))

                pygame.display.flip()

                # Отображение кадра с захваченной рукой
                cv2.imshow('Hand Tracking', image)

                key = cv2.waitKey(1)
                if key == 27:
                    game_over = True

                clock.tick(snake_speed)


    cv2.destroyAllWindows()
    cap.release()
    pygame.quit()


