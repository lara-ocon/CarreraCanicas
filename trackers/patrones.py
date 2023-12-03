import cv2
from picamera2 import Picamera2
import numpy as np

# Rangos de colores en HSV
LOWER_COLOR_BLUE = np.array([90, 50, 50])
UPPER_COLOR_BLUE = np.array([130, 255, 255])

LOWER_COLOR_YELLOW = np.array([20, 100, 100])
UPPER_COLOR_YELLOW = np.array([30, 255, 255])

LOWER_COLOR_GREEN = np.array([40, 100, 100])
UPPER_COLOR_GREEN = np.array([80, 255, 255])

LOWER_COLOR_RED1 = np.array([0, 100, 100])
UPPER_COLOR_RED1 = np.array([10, 255, 255])

LOWER_COLOR_RED2 = np.array([170, 100, 100])
UPPER_COLOR_RED2 = np.array([180, 255, 255])

LOWER_COLOR_BLACK = np.array([0, 0, 0])
UPPER_COLOR_BLACK = np.array([180, 255, 30])

LOWER_COLOR_ORANGE = np.array([5, 100, 100])
UPPER_COLOR_ORANGE = np.array([15, 255, 255])


# TRACKER CUADRADO AMARILLO
def tracker_cuadrado_amarillo(frame, prev_x, prev_y, trajectory, is_tracking):
    # Convertir el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # color en HSV (amarillo)
    lower_color = LOWER_COLOR_YELLOW
    upper_color = UPPER_COLOR_YELLOW

    # Crear una máscara para el color que nos pasan y aplicarla al frame
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se detecta algún contorno comprobamos que sea un cuadrado
    if contours:

        # Encontrar el contorno más grande (cuadrado)
        largest_contour = max(contours, key=cv2.contourArea)

        # Encontrar el perímetro del contorno
        perimeter = cv2.arcLength(largest_contour, True)

        # Aproximar el contorno a un polígono
        approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)

        # Si el polígono tiene 4 vértices, es un cuadrado
        if len(approx) == 4:
            # Encontrar el rectángulo más pequeño que contiene el polígono
            x, y, w, h = cv2.boundingRect(approx)

            # Dibujar el rectángulo y su centro
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Dibujar la trayectoria
            if prev_x is not None and prev_y is not None:
                cv2.line(frame, (prev_x, prev_y), (x + w // 2, y + h // 2), (0, 0, 255), 5)
                cv2.putText(frame, "1", (x + w // 2, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Almacenar las coordenadas para la trayectoria
                if is_tracking == True:
                    trajectory.append((x + w // 2, y + h // 2))

            # Actualizar las coordenadas previas
            prev_x, prev_y = x + w // 2, y + h // 2

    return frame, prev_x, prev_y, trajectory


def tracker_triangulo_azul(frame, prev_x, prev_y, trajectory, is_tracking):

    # Convertir el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # color en HSV (azul)
    lower_color = LOWER_COLOR_BLUE
    upper_color = UPPER_COLOR_BLUE

    # Crear una máscara para el color que nos pasan y aplicarla al frame
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se detecta algún contorno comprobamos que sea un triángulo
    if contours:

        # Encontrar el contorno más grande (triángulo)
        largest_contour = max(contours, key=cv2.contourArea)

        # Encontrar el perímetro del contorno
        perimeter = cv2.arcLength(largest_contour, True)

        # Aproximar el contorno a un polígono
        approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)

        # Si el polígono tiene 3 vértices, es un triángulo
        if len(approx) == 3:
            # Encontrar el rectángulo más pequeño que contiene el polígono
            x, y, w, h = cv2.boundingRect(approx)

            # Dibujar el rectángulo y su centro
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Dibujar la trayectoria
            if prev_x is not None and prev_y is not None:
                cv2.line(frame, (prev_x, prev_y), (x + w // 2, y + h // 2), (0, 0, 255), 5)
                cv2.putText(frame, "2", (x + w // 2, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Almacenar las coordenadas para la trayectoria
                if is_tracking == True:
                    trajectory.append((x + w // 2, y + h // 2))

            # Actualizar las coordenadas previas
            prev_x, prev_y = x + w // 2, y + h // 2

    return frame, prev_x, prev_y, trajectory


def tracker_circulo_verde(frame, prev_x, prev_y, trajectory, is_tracking):

    # Convertir el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # color en HSV (rojo)
    lower_color = LOWER_COLOR_GREEN
    upper_color = UPPER_COLOR_GREEN

    # Crear una máscara para el color que nos pasan y aplicarla al frame
    mask1 = cv2.inRange(hsv, lower_color, upper_color)
    mask2 = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se detecta algún contorno comprobamos que sea un círculo
    if contours:
        # Encontrar el contorno más grande (círculo)
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        # Asegurarse de que el radio sea lo suficientemente grande para ser considerado como el círculo
        if radius > 10:
            # Convertir las coordenadas a números enteros
            x, y, radius = int(x), int(y), int(radius)
            # Dibujar el círculo y su centro
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            # Dibujar la trayectoria
            if prev_x is not None and prev_y is not None:
                cv2.line(frame, (prev_x, prev_y), (x, y), (0, 0, 255), 5)
                cv2.putText(frame, "3", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                # Almacenar las coordenadas para la trayectoria
                if is_tracking == True:
                    trajectory.append((x, y))
            # Actualizar las coorden
            prev_x, prev_y = x, y

    return frame, prev_x, prev_y, trajectory



# Dibujar la trayectoria del objeto en el frame
def draw_trajectory(frame, trajectory):
    # Dibujar la trayectoria almacenada
    for i in range(1, len(trajectory)):
        cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 255, 0), 15)
    return frame

def stream_video():

    picam = Picamera2()
    picam.video_configuration.main.size = (640, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    prev_x, prev_y = None, None
    trajectory = []
    is_tracking = False
    while True:
        frame = picam.capture_array()
        
        # Realizar el seguimiento de de los objetos
        frame, prev_x, prev_y, trajectory1 = tracker_cuadrado_amarillo(frame, prev_x, prev_y, trajectory, is_tracking)
        frame, prev_x, prev_y, trajectory2 = tracker_triangulo_azul(frame, prev_x, prev_y, trajectory, is_tracking)
        frame, prev_x, prev_y, trajectory3 = tracker_circulo_verde(frame, prev_x, prev_y, trajectory, is_tracking)

        # frame_with_trajectory = draw_trajectory(frame.copy(), trajectory)

        cv2.imshow("picam", frame)

        # Detectar tecla pulsada
        key = cv2.waitKey(1)
        if key == ord('s'):
            is_tracking = True
        elif key == ord('e'):
            is_tracking = False
            trajectory = []
            prev_x = None
            prev_y = None
        elif key == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":

    stream_video()