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

# TRACKER
def tracker(frame, prev_x, prev_y, trajectory, is_tracking):
    # Convertir el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # color en HSV (azul)
    lower_color = LOWER_COLOR_YELLOW
    upper_color = UPPER_COLOR_YELLOW

    # Crear una máscara para el color que nos pasan y aplicarla al frame
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se detecta algún contorno
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
                # Almacenar las coordenadas para la trayectoria
                if is_tracking == True:
                    trajectory.append((x, y))
            # Actualizar las coordenadas previas
            prev_x, prev_y = x, y
    return frame, prev_x, prev_y, trajectory


# Dibujar la trayectoria del objeto en el frame
def draw_trajectory(frame, trajectory):

    # primero interpolamos la trayectoria para que sea mas

    smooth_trajectory = []
    for i in range(1, len(trajectory)):
        x1, y1 = trajectory[i-1]
        x2, y2 = trajectory[i]
        smooth_trajectory.append((x1, y1))
        smooth_trajectory.append(((x1 + x2) // 2, (y1 + y2) // 2))

    # Dibujar la trayectoria almacenada
    for i in range(1, len(trajectory)):
        cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 255, 0), 15)
    return frame


# Funcion para dibujar 1 cuadrado sobre el video
def overlay_square(frame):
    # Dibujar un cuadrado en el centro y muy grande
    centro = (frame.shape[1] // 2, frame.shape[0] // 2)
    cv2.rectangle(frame, (centro[0] - 100, centro[1] - 100), (centro[0] + 100, centro[1] + 100), (255, 0, 0), 20)
    return frame


# Funcion para dibujar un triangulo centrado y más grande sobre el video
def overlay_large_triangle(frame):
    # Definir los vértices del triángulo más grande
    pts = np.array([[100, 300], [200, 100], [300, 300]], np.int32)
    pts = pts.reshape((-1, 1, 2))

    # Escalar los vértices del triángulo para hacerlo más grande y centrado
    scale_factor = 2  # Factor de escala para agrandar el triángulo
    center_offset = [frame.shape[1] // 2 - 150, frame.shape[0] // 2 - 100]  # Desplazamiento para centrar el triángulo

    scaled_pts = pts * scale_factor
    translated_pts = scaled_pts + center_offset

    # Dibujar el triángulo más grande
    cv2.polylines(frame, [translated_pts], True, (0, 255, 255), 20)
    return frame



# Funcion para dibujar el logo de disney
def overlay_disney_logo(frame):
    # Cargar la imagen del logo de Disney Channel con transparencia
    disney_logo = cv2.imread('disney-channel-logo.png', -1)  # Ruta de la imagen del logo

    # giramos el logo horizontalmente(porque luego voltearemos el frame)
    disney_logo = disney_logo[:, ::-1, :]

    # Extraer los canales R, G, B de la imagen del logo y el canal alfa
    logo_bgr = disney_logo[:, :, 0:3]
    logo_mask = disney_logo[:, :, 3]

    # Redimensionar el logo de Disney Channel para que se ajuste al tamaño deseado (más grande)
    logo_resized = cv2.resize(logo_bgr, (400, 400))  # Ajusta el tamaño según sea necesario

    # Redimensionar la máscara del logo para que coincida con el tamaño del logo
    logo_mask_resized = cv2.resize(logo_mask, (400, 400))

    # Obtener las coordenadas donde se superpondrá el logo en la esquina inferior
    # lo ponemos en la esquina inferior derecha (despues voltearemos el frame para que se vea en la izquierda)
    y1, y2 = frame.shape[0] - logo_resized.shape[0], frame.shape[0]  # Esquina inferior
    # x1, x2 = 0, logo_resized.shape[1]  # Esquina izquierda
    x1, x2 = frame.shape[1] - logo_resized.shape[1], frame.shape[1]  # Esquina derecha


    # Verificar que las coordenadas no excedan las dimensiones de la imagen en blanco
    if y2 - y1 <= frame.shape[0] and x2 - x1 <= frame.shape[1]:
        # Superponer el logo en la esquina inferior del video respetando la transparencia
        for c in range(0, 3):
            frame[y1:y2, x1:x2, c] = (logo_resized[:, :, c] * (logo_mask_resized / 255.0)) + \
                                     (frame[y1:y2, x1:x2, c] * (1.0 - (logo_mask_resized / 255.0)))

    else:
        print("Las coordenadas de superposición exceden las dimensiones del video.")
    
    return frame


# Función para comparar la trayectoria con el cuadrado
def compare_trajectory(trajectory, shape):
    # Crear un cuadrado perfecto en una imagen en blanco
    img1 = np.zeros((640, 480, 3), np.uint8)
    centro = (img1.shape[1] // 2, img1.shape[0] // 2)
    threshold = 0

    if shape == "square":
        cv2.rectangle(img1, (centro[0] - 100, centro[1] - 100), (centro[0] + 100, centro[1] + 100), (255, 0, 0), 20)
        threshold = 0.08
    elif shape == "triangle":
        img1 = overlay_large_triangle(img1)
        threshold = 0.6
    elif shape == "disney":
        overlay_disney_logo(img1)
        threshold = 5

    # Crear una imagen en blanco y dibujar la trayectoria
    img2 = np.zeros((640, 480, 3), np.uint8)
    img2 = draw_trajectory(img2, trajectory)

    # Convertir imágenes a escala de grises
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Encontrar contornos en ambas imágenes
    contours1, _ = cv2.findContours(gray1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(gray2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Obtener el contorno del cuadrado perfecto
    contour1 = max(contours1, key=cv2.contourArea)
    
    # Calcular la distancia entre los contornos del cuadrado y la trayectoria
    distances = [cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I2, 0.0) for contour2 in contours2]

    if len(distances) == 0:
        return False
    
    # Si la distancia más pequeña es menor a un umbral, consideramos que el cuadrado está bien
    min_distance = min(distances)
    print(min_distance)
    if min_distance < threshold:  # Ajusta el umbral según sea necesario
        return True
    else:
        return False
    

def complete_figure(figure):

    prev_x, prev_y = None, None
    trajectory = []
    is_tracking = False
    texto = 'Pulsa "s" para comenzar a dibujar'
    while True:
        frame = picam.capture_array()
        
        # Realizar el seguimiento de de los objetos
        frame, prev_x, prev_y, trajectory = tracker(frame, prev_x, prev_y, trajectory, is_tracking)

        # Dibujar la forma que sea
        if figure == "square":
            frame_with_figure = overlay_square(frame)
        elif figure == "triangle":
            frame_with_figure = overlay_triangle(frame)
        elif figure == "disney":
            frame_with_figure = overlay_disney_logo(frame)

        # Dibujar la trayectoria en el frame
        frame_with_trajectory = draw_trajectory(frame_with_figure.copy(), trajectory)

        # flipeamos
        frame_flipped = cv2.flip(frame_with_trajectory, 1)

        # Mostramos mensaje
        cv2.putText(frame_flipped, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("picam", frame_flipped)


        # Detectar tecla pulsada
        key = cv2.waitKey(1)
        if key == ord('s'):
            is_tracking = True
            texto = 'Pulsa "e" para terminar de dibujar'
        elif key == ord('e'):
            # comprobamos si la trayectoria esta bien
            if compare_trajectory(trajectory, figure):
                texto = "La figura esta bien"
            else:
                texto = "La figura esta mal"

            is_tracking = False
            trajectory = []
            prev_x = None
            prev_y = None
        elif key == ord('q'):
            break

if __name__ == "__main__":

    picam = Picamera2()
    picam.video_configuration.main.size = (640, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    
    complete_figure("disney")

    cv2.destroyAllWindows()