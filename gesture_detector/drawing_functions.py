import cv2  # Importa OpenCV para manipulación de imágenes y vídeos
import numpy as np  # Importa NumPy para operaciones numéricas eficientes

class DrawingFunctions:
    def __init__(self):
        # Inicializa imágenes para diferentes acciones utilizando rutas relativas
        self.img_forward = cv2.imread('gesture_detector/resources/images/forward.png')
        self.img_reverse = cv2.imread('gesture_detector/resources/images/reverse.png')
        self.img_left = cv2.imread('gesture_detector/resources/images/left.png')
        self.img_right = cv2.imread('gesture_detector/resources/images/right.png')
        self.img_stop = cv2.imread('gesture_detector/resources/images/stop.png')

    def draw_image(self, original_frame: np.ndarray, action_image: np.ndarray):
        # Dibuja una imagen de acción sobre el marco original en una posición específica
        ah, aw, _ = action_image.shape  # Obtiene dimensiones de la imagen de acción
        original_frame[600:600 + ah, 50:50 + aw] = action_image  # Coloca la imagen de acción en el marco original
        return original_frame  # Retorna el marco modificado

    def draw_actions(self, action: str, original_frame: np.ndarray) -> np.ndarray:
        # Dibuja una imagen de acción específica en el marco original según el comando recibido

        # Define un diccionario que mapea comandos de acción a imágenes correspondientes
        actions_dict = {
            'A': self.img_forward,  # 'A' representa avanzar
            'P': self.img_stop,     # 'P' representa detenerse
            'I': self.img_left,     # 'I' representa girar a la izquierda
            'D': self.img_right,    # 'D' representa girar a la derecha
            'R': self.img_reverse,  # 'R' representa reversa
        }

        # Verifica si el comando recibido está en el diccionario de acciones
        if action in actions_dict:
            movement_image = actions_dict[action]  # Obtiene la imagen correspondiente al comando
            original_frame = self.draw_image(original_frame, movement_image)  # Dibuja la imagen en el marco original

        return original_frame  # Retorna el marco original modificado (o no modificado si el comando no está presente)