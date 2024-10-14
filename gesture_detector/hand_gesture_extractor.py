import math  # Importa la biblioteca math para operaciones matemáticas
import cv2  # Importa OpenCV para manipulación de imágenes y vídeos
import numpy as np  # Importa NumPy para operaciones numéricas eficientes
import mediapipe as mp  # Importa Mediapipe para procesamiento de visión por computadora
from typing import List, Tuple  # Importa List y Tuple para anotaciones de tipo

class HandProcessing:
    def __init__(self, mode=False, hands=1, model_complexity=0, threshold_detection=0.5, threshold_tracking=0.5):
        # Inicializa los parámetros del objeto HandProcessing
        self.mode = mode  # Modo de detección (por defecto False)
        self.max_hands = hands  # Máximo número de manos a detectar
        self.complexity = model_complexity  # Complejidad del modelo
        self.conf_detection = threshold_detection  # Umbral de confianza de detección
        self.conf_tracking = threshold_tracking  # Umbral de confianza de seguimiento

        # Inicializa el modelo de detección de manos de Mediapipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.complexity, self.conf_detection, self.conf_tracking)
        self.draw = mp.solutions.drawing_utils  # Utilidad de dibujo de Mediapipe
        self.tip = [4, 8, 12, 16, 20]  # Índices de las puntas de los dedos

    def find_hands(self, frame: np.ndarray, draw: bool = True) -> np.ndarray:
        # Convierte la imagen a formato RGB (Mediapipe requiere RGB)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Procesa la imagen para detectar manos
        self.results = self.hands.process(img_rgb)

        # Si se detectan landmarks de manos, dibuja los puntos y conexiones en la imagen
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame  # Retorna la imagen con las manos detectadas y marcadas

    def find_position(self, frame: np.ndarray, hand: int = 0, draw_points: bool = True, draw_box: bool = True, color: List[int] = []) \
            -> Tuple[List[List[int]], Tuple[int, int, int, int]]:
        xlist: List[int] = []  # Lista para almacenar coordenadas x de landmarks
        ylist: List[int] = []  # Lista para almacenar coordenadas y de landmarks
        bbox: Tuple[int, int, int, int] = ()  # Bounding box (rectángulo delimitador)
        hands_list: List[List[int]] = []  # Lista para almacenar información de landmarks

        # Si se detectan landmarks de manos múltiples
        if self.results.multi_hand_landmarks:
            # Obtén los landmarks de la mano especificada por el índice `hand`
            my_hand = self.results.multi_hand_landmarks[hand]
            for id, lm in enumerate(my_hand.landmark):
                height, width, c = frame.shape  # Obtiene dimensiones de la imagen
                cx, cy = int(lm.x * width), int(lm.y * height)  # Calcula las coordenadas de landmark en píxeles
                xlist.append(cx)  # Agrega la coordenada x a la lista
                ylist.append(cy)  # Agrega la coordenada y a la lista
                hands_list.append([id, cx, cy])  # Agrega información de landmark a la lista

                # Si se solicita, dibuja puntos en los landmarks
                if draw_points:
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 0), cv2.FILLED)

            # Calcula el bounding box que encierra todas las manos detectadas
            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            bbox = xmin, ymin, xmax, ymax

            # Si se solicita, dibuja un rectángulo alrededor del bounding box
            if draw_box:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), color, 2)

        return hands_list, bbox  # Retorna la lista de landmarks y el bounding box

    def fingers_up(self, keypoints_list: List[List[int]]) -> List[int]:
        fingers: List[int] = []  # Lista para almacenar el estado de los dedos levantados

        # Comprueba si el pulgar está levantado
        if keypoints_list[self.tip[0]][1] > keypoints_list[self.tip[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Comprueba el estado de los otros cuatro dedos
        for i in range(1, 5):
            if keypoints_list[self.tip[i]][2] < keypoints_list[self.tip[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers  # Retorna la lista con el estado de los dedos levantados

    def distance(self, p1: int, p2: int, frame: np.ndarray, draw: bool = True, radius: int = 15, thickness: int = 3) \
            -> Tuple[float, np.ndarray, list]:
        # Obtiene las coordenadas de los puntos p1 y p2
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        
        # Calcula el punto medio y dibuja una línea y círculos si se solicita
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness)
            cv2.circle(frame, (x1, y1), radius, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), radius, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), radius, (0, 0, 255), cv2.FILLED)

        # Calcula la longitud de la línea entre p1 y p2
        length = math.hypot(x2 - x1, y2 - y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]  # Retorna la longitud, la imagen con los elementos dibujados y las coordenadas