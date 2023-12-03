import cv2
from picamera2 import Picamera2
import numpy as np

# Rangos de colores en HSV
LOWER_COLOR_BLUE = np.array([90, 50, 50])
UPPER_COLOR_BLUE = np.array([130, 255, 255])

# TRACKER
def tracker(frame, prev_x, prev_y, trajectory, is_tracking):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = LOWER_COLOR_BLUE
    upper_color = UPPER_COLOR_BLUE
    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        if radius > 10:
            x, y, radius = int(x), int(y), int(radius)
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            if prev_x is not None and prev_y is not None:
                cv2.line(frame, (prev_x, prev_y), (x, y), (0, 0, 255), 5)
                if is_tracking == True:
                    trajectory.append((x, y))
            prev_x, prev_y = x, y
    return frame, prev_x, prev_y, trajectory

# Función para dibujar la trayectoria del objeto en el frame
def draw_trajectory(frame, trajectory):
    for i in range(1, len(trajectory)):
        cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 255, 0), 15)
    return frame

# Función para dibujar un círculo azul en el centro de la imagen
def draw_blue_circle(frame):
    height, width = frame.shape[:2]
    center_coordinates = (width // 2, height // 2)
    radius = 100
    color = (255, 0, 0)
    thickness = 15
    cv2.circle(frame, center_coordinates, radius, color, thickness)

# Calcular la distancia euclidiana entre dos puntos
def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Función para comprobar si la trayectoria coincide con el círculo azul
def check_similarity(trajectory):
    height, width = 480, 640
    center_coordinates = (width // 2, height // 2)
    radius = 100
    circle_points = []

    for angle in range(0, 360, 5):
        x = int(center_coordinates[0] + radius * np.cos(np.radians(angle)))
        y = int(center_coordinates[1] + radius * np.sin(np.radians(angle)))
        circle_points.append((x, y))

    threshold = 30
    similarity = all(
        euclidean_distance(trajectory[i], circle_points[i]) < threshold
        for i in range(min(len(trajectory), len(circle_points)))
    )

    return similarity

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
    texto_video = "Pulsa 's' para empezar a dibujar"
    while True:
        frame = picam.capture_array()
        
        frame, prev_x, prev_y, trajectory = tracker(frame, prev_x, prev_y, trajectory, is_tracking)
        draw_blue_circle(frame)
        frame_with_trajectory = draw_trajectory(frame.copy(), trajectory)

        key = cv2.waitKey(1)
        if key == ord('s'):
            texto_video = "Pulsa 'e' para dejar de dibujar"
            is_tracking = True
        elif key == ord('e'):
            is_tracking = False
            if check_similarity(trajectory):
                texto_video = "¡Has dibujado un círculo!"
                trajectory = []
                prev_x = None
                prev_y = None
            else:
                texto_video = "¡Ohhh vuelvelo a intentar!"
                trajectory = []
        elif key == ord('q'):
            break

        frame_with_text = cv2.putText(frame_with_trajectory, texto_video, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("picam", frame_with_text)
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()
