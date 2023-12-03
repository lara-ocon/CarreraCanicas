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

    x, y, w, h = None, None, None, None

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
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Dibujar la trayectoria
            if prev_x is not None and prev_y is not None:
                # cv2.line(frame, (prev_x, prev_y), (x + w // 2, y + h // 2), (0, 0, 255), 5)
                # cv2.putText(frame, "1", (x + w // 2, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Almacenar las coordenadas para la trayectoria
                if is_tracking == True:
                    trajectory.append((x + w // 2, y + h // 2))

            # Actualizar las coordenadas previas
            prev_x, prev_y = x + w // 2, y + h // 2

    return frame, prev_x, prev_y, trajectory, x, y, w, h


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

    x, y, w, h = None, None, None, None

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

            # Guardar la trayectoria
            if prev_x is not None and prev_y is not None:

                # Almacenar las coordenadas para la trayectoria
                if is_tracking == True:
                    trajectory.append((x + w // 2, y + h // 2))

            # Actualizar las coordenadas previas
            prev_x, prev_y = x + w // 2, y + h // 2

    return frame, prev_x, prev_y, trajectory, x, y, w, h


def tracker_circulo_verde(frame, prev_x, prev_y, trajectory, is_tracking):

    # Convertir el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # color en HSV (rojo)
    lower_color = LOWER_COLOR_BLUE
    upper_color = UPPER_COLOR_BLUE

    # Crear una máscara para el color que nos pasan y aplicarla al frame
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y, radius = None, None, 0

    # Si se detecta algún contorno comprobamos que sea un círculo
    if contours:

        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
            else:
                circularity = 0

            if circularity > 0.85:  # Ajusta este umbral según tu definición de casi perfecto
                ((x, y), radius_new) = cv2.minEnclosingCircle(contour)

                if radius_new > 30 and radius_new > radius:
                    radius = radius_new
                    print('He detectado un circulo')
                    # Convertir las coordenadas a números enteros
                    x, y, radius = int(x), int(y), int(radius)
                    # Dibujar el círculo y su centro
                    # cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
                    # cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

                    if is_tracking == True:
                        trajectory.append((x, y))

                    # Actualizar las coorden
                    prev_x, prev_y = x, y

                    break # termina el bucle si encuentra un buen circulo
    
    if radius == 0:
        radius = None

    return frame, prev_x, prev_y, trajectory, x, y, radius


def dibujar_objeto(frame, x, y, w, h, type, prev_x, prev_y, trajectory, is_tracking):

    # en el circulo, w y h son el radio
    if type == "cuadrado":
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    elif type == "triangulo":
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    elif type == "circulo":
        cv2.circle(frame, (x,y), w, (0, 255, 0), 2)
        cv2.circle(frame, (x,y), 5, (0, 0, 255), -1)

    # ponemos el tipo de objeto
    cv2.putText(frame, type, (x + w // 2, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # dibujamos la trayectoria
    cv2.line(frame, (prev_x, prev_y), (x + w // 2, y + h // 2), (0, 0, 255), 5)

    return frame

    
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
    prev_x1, prev_y1 = None, None
    prev_x2, prev_y2 = None, None
    prev_x3, prev_y3 = None, None
    trajectory1 = []
    trajectory2 = []
    trajectory3 = []
    trajectories = [trajectory1, trajectory2, trajectory3]
    prev_x = [prev_x1, prev_x2, prev_x3]
    prev_y = [prev_y1, prev_y2, prev_y3]
    is_tracking = False
    while True:
        frame = picam.capture_array()
        
        # Realizar el seguimiento de de los objetos
        frame, prev_x1, prev_y1, trajectory1, x1, y1, w1, h1 = tracker_cuadrado_amarillo(frame, prev_x1, prev_y1, trajectory1, is_tracking)
        frame, prev_x2, prev_y2, trajectory2, x2, y2, w2, h2 = tracker_triangulo_azul(frame, prev_x2, prev_y2, trajectory2, is_tracking)
        frame, prev_x3, prev_y3, trajectory3, x3, y3, radius = tracker_circulo_verde(frame, prev_x3, prev_y3, trajectory3, is_tracking)

        # Dibubjamos los objetos
        if x1 is not None and y1 is not None:
            frame = dibujar_objeto(frame, x1, y1, w1, h1, "cuadrado", prev_x1, prev_y1, trajectory1, is_tracking)
        
        if x2 is not None and y2 is not None:
            frame = dibujar_objeto(frame, x2, y2, w2, h2, "triangulo", prev_x2, prev_y2, trajectory2, is_tracking)

        if None not in [x3, y3, radius]:
            frame = dibujar_objeto(frame, x3, y3, radius, radius, "circulo", prev_x3, prev_y3, trajectory3, is_tracking)

        cv2.imshow("picam", frame)

        # Detectar tecla pulsada
        key = cv2.waitKey(1)
        if key == ord('s'):
            is_tracking = True
        elif key == ord('e'):
            is_tracking = False
            
            # reiniciamos las trayectorias
            for i in range(len(trajectories)):
                trajectories[i] = []
                prev_x[i] = None
                prev_y[i] = None

        elif key == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":

    stream_video()