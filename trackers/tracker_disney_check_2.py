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
    # Dibujar la trayectoria almacenada
    for i in range(1, len(trajectory)):
        cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 255, 0), 15)
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


def compare_shapes(trajectory, contour_logo):

    similarity = 1000
    # Calcular el contorno de la trayectoria actual
    if len(trajectory) > 10:  # Calcular el contorno solo si hay suficientes puntos en la trayectoria
        pts = np.array(trajectory[-10:], dtype=np.int32)  # Usar los últimos 10 puntos de la trayectoria
        contour_trajectory = cv2.convexHull(pts) # Calcular el contorno convexo de los puntos

        # Calcular la similitud entre los contornos
        similarity = cv2.matchShapes(contour_logo, contour_trajectory, cv2.CONTOURS_MATCH_I2, 0.0)

    return similarity


def obtain_logo_mask_resized():
    
    disney_logo = cv2.imread('disney-channel-logo.png', -1)  # Ruta de la imagen del logo
    disney_logo_gray = cv2.cvtColor(disney_logo, cv2.COLOR_BGR2GRAY)
    _, disney_logo_thresh = cv2.threshold(disney_logo_gray, 1, 255, cv2.THRESH_BINARY)
    contours_logo, _ = cv2.findContours(disney_logo_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_logo = max(contours_logo, key=cv2.contourArea)

    # Redimensionar la máscara del logo para que coincida con el tamaño del logo
    logo_mask_resized = cv2.resize(disney_logo_thresh, (400, 400))

    return logo_mask_resized

def obtain_logo_contour(logo_mask_resized):

    disney_logo = cv2.imread('disney-channel-logo.png', -1)  # Ruta de la imagen del logo
    disney_logo_gray = cv2.cvtColor(disney_logo, cv2.COLOR_BGR2GRAY)
    _, disney_logo_thresh = cv2.threshold(disney_logo_gray, 1, 255, cv2.THRESH_BINARY)
    contours_logo, _ = cv2.findContours(disney_logo_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_logo = max(contours_logo, key=cv2.contourArea)

    return contour_logo

def stream_video():
    picam = Picamera2()
    picam.video_configuration.main.size = (640, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    is_tracking = False
    prev_x, prev_y = None, None
    trajectory = []

    logo_mask_resized = obtain_logo_mask_resized()
    contour_logo = obtain_logo_contour(logo_mask_resized)

    while True:
        frame = picam.capture_array()
        
        # Realizar el seguimiento del círculo
        frame, prev_x, prev_y, trajectory = tracker(frame, prev_x, prev_y, trajectory, is_tracking)

        # Calcular la similitud entre la trayectoria y el logo
        similarity = compare_shapes(trajectory, contour_logo)

        # Superponer el logo de Disney Channel en el video
        frame_with_logo = overlay_disney_logo(frame)

        # Dibujar la trayectoria en el frame
        frame_with_trajectory = draw_trajectory(frame_with_logo.copy(), trajectory)

        # ponemos si se ha conseguido
        if similarity < 0.1:
            cv2.putText(frame_with_trajectory, "CONSEGUIDO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            print(f'Porcentaje de similitud: {similarity}')

        # Mostrar el frame
        frame_flipped = frame_with_trajectory[:, ::-1, :]  # Voltear el frame horizontalmente
        cv2.imshow("picam", frame_flipped)

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
