# Este script será capaz de detectar o bien:
# - 1 circulo verde
# - 1 cuadrado amarillo
# - 1 triangulo azul

# Trackeará dicha forma y si el usuario pulsa la tecla 's' se quedará con esa forma y finalizará el programa.
import cv2
import numpy as np
from picamera2 import Picamera2

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
def tracker_cuadrado_amarillo(frame, prev_x, prev_y):

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
    
            # Actualizar las coordenadas previas
            prev_x, prev_y = x + w//2, y + h//2
    
    return frame, prev_x, prev_y, x, y, w, h

# TRACKER TRIANGULO VERDE
def tracker_triangulo_naranja(frame, prev_x, prev_y):
    
        # Convertir el frame de BGR a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # color en HSV (azul)
        lower_color = LOWER_COLOR_ORANGE
        upper_color = UPPER_COLOR_ORANGE
    
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
        
                # Actualizar las coordenadas previas
                prev_x, prev_y = x + w//2, y + h//2
        
        return frame, prev_x, prev_y, x, y, w, h


def tracker_circulo_azul(frame, prev_x, prev_y):

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
                    # Convertir las coordenadas a números enteros
                    x, y, radius = int(x), int(y), int(radius)

                    # Actualizar las coorden
                    prev_x, prev_y = x, y

                    break # termina el bucle si encuentra un buen circulo
    
    if radius == 0:
        radius = None

    return frame, prev_x, prev_y, x, y, radius, radius


def dibujar_forma(tipo, x, y, w, h, frame):

    # pintamos la forma
    if tipo == 'square':
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # pintamos un punto en el centro
        cv2.circle(frame, (x + w//2, y + h//2), 5, (0, 0, 255), -1)

    elif tipo == 'triangulo':
        # Dibujae un triangulo
        points = np.array([[x + w//2, y], [x, y + h], [x + w, y + h]])
        cv2.drawContours(frame, [points], 0, (0, 0, 255), 2)

        # pintamos un punto en el centro
        cv2.circle(frame, (x + w//2, y + h//2), 5, (0, 0, 255), -1)

    elif tipo == 'circulo':
        try: 
            cv2.circle(frame, (x, y), w, (0, 255, 0), 2)

            # pintamos un punto en el centro
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        except:
            pass


def tracker_objetos(picam, output_video):

    # Inicializamos las coordenadas previas de los 4 objetos
    prev_x_cuadrado, prev_y_cuadrado = None, None
    prev_x_triangulo, prev_y_triangulo = None, None
    prev_x_circulo, prev_y_circulo = None, None

    # Inicializamos las coordenadas de los 4 objetos
    x_cuadrado, y_cuadrado = None, None
    x_triangulo, y_triangulo = None, None
    x_circulo, y_circulo = None, None

    # Inicializamos los tamaños de los 4 objetos
    w_cuadrado, h_cuadrado = None, None
    w_triangulo, h_triangulo = None, None
    w_circulo, h_circulo = None, None

    while True:
        frame = picam.capture_array()
        
        # Rastreamos los 4 objetos
        frame, prev_x_cuadrado, prev_y_cuadrado, x_cuadrado, y_cuadrado, w_cuadrado, h_cuadrado = tracker_cuadrado_amarillo(frame, prev_x_cuadrado, prev_y_cuadrado)
        frame, prev_x_triangulo, prev_y_triangulo, x_triangulo, y_triangulo, w_triangulo, h_triangulo = tracker_triangulo_naranja(frame, prev_x_triangulo, prev_y_triangulo)
        frame, prev_x_circulo, prev_y_circulo, x_circulo, y_circulo, w_circulo, h_circulo = tracker_circulo_azul(frame, prev_x_circulo, prev_y_circulo)

        # Dibujamos los objetos encontrados
        if x_cuadrado is not None and y_cuadrado is not None:
            dibujar_forma('cuadrado', x_cuadrado, y_cuadrado, w_cuadrado, h_cuadrado, frame)
        if x_triangulo is not None and y_triangulo is not None:
            dibujar_forma('triangulo', x_triangulo, y_triangulo, w_triangulo, h_triangulo, frame)
        if x_circulo is not None and y_circulo is not None:
            dibujar_forma('circulo', x_circulo, y_circulo, w_circulo, h_circulo, frame)
        
        # Mostramos el frame
        cv2.imshow("picam", frame[:, ::-1, :])

        # Guardamos el frame en el video
        output_video.write(frame)

        # Si se pulsa una tecla y en ese momento solo hay 1 objeto en pantalla
        # nos quedamos con ese objeto y salimos del bucle
        key = cv2.waitKey(1)
        if key == ord('s'):
            if sum([x_cuadrado is not None, x_triangulo is not None, x_circulo is not None]) == 1:
                if x_cuadrado is not None:
                    return 'square', False
                elif x_triangulo is not None:
                    return 'triangle', False
                elif x_circulo is not None:
                    return 'disney', False
        elif key == ord('q'):
            break
        
    return None, True # forma None, salir True

    
if __name__ == "__main__":

    picam = Picamera2()
    picam.video_configuration.main.size = (640, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    output_file = "output_video_formas.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    output_video = cv2.VideoWriter(output_file, fourcc, fps, (640, 480))

    # Trackeamos los objetos
    forma, salir = tracker_objetos(picam, output_video)

    print("La forma es: ", forma)

    output_video.release()

    cv2.destroyAllWindows()
    picam.stop()