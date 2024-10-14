import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas eficientes
from typing import List, Tuple  # Importa List y Tuple para anotaciones de tipo

# Importa las clases HandProcessing y DrawingFunctions desde los módulos correspondientes
from gesture_detector.hand_gesture_extractor import HandProcessing
from gesture_detector.drawing_functions import DrawingFunctions

class GestureDetector:
    def __init__(self):
        # Inicializa el objeto hand_detector con umbral de detección de manos de 0.9
        self.hand_detector = HandProcessing(threshold_detection=0.9)
        # Inicializa el objeto draw para realizar funciones de dibujo
        self.draw = DrawingFunctions()

    def fingers_interpretation(self, fingers_up: List[int]) -> str:
        # Define un diccionario que mapea configuraciones de dedos levantados a comandos
        commands = {
            (0, 0, 0, 0, 0): 'A',   # Ningún dedo levantado -> 'A'
            (1, 1, 1, 1, 1): 'P',   # Todos los dedos levantados -> 'P'
            (1, 0, 0, 0, 0): 'I',   # Solo el pulgar levantado -> 'I'
            (0, 0, 0, 0, 1): 'D',   # Solo el meñique levantado -> 'D'
            (1, 0, 0, 0, 1): 'R',   # Pulgar y meñique levantados -> 'R'
        }
        # Retorna el comando correspondiente según la configuración de dedos levantados
        return commands.get(tuple(fingers_up), "")

    def gesture_interpretation(self, img: np.ndarray) -> Tuple[str, np.ndarray]:
        frame = img.copy()  # Copia la imagen de entrada para no modificar la original
        frame = self.hand_detector.find_hands(frame, draw=True)  # Detecta y marca las manos en la imagen
        hand_list, bbox = self.hand_detector.find_position(frame, draw_box=False)  # Localiza las posiciones de las manos
        if len(hand_list) == 21:  # Si se detectan las 21 articulaciones de la mano
            fingers_up = self.hand_detector.fingers_up(hand_list)  # Determina qué dedos están levantados
            command = self.fingers_interpretation(fingers_up)  # Interpreta el gesto basado en los dedos levantados
            frame = self.draw.draw_actions(command, frame)  # Dibuja la acción correspondiente en la imagen
            return command, frame  # Retorna el comando interpretado y la imagen modificada
        else:
            return "P", frame  # Si no se detectan las 21 articulaciones, retorna un comando predeterminado y la imagen original
