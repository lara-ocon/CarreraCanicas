import detector 
import cv2
import calibration
import tracker_disney_check_2 as disney_tracker
from picamera2 import Picamera2


def iniciar_grabacion():
    picam = Picamera2()
    picam.video_configuration.main.size = (640, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    return picam


if __name__ == "__main__":

    print("Pulsa para comenzar la detección de la secuencia")

    picam = iniciar_grabacion()

    # 1) Detectar la secuencia de patrones
    patron, not_patron = detector.obtener_patrones()
    desbloqueado = False

    while not desbloqueado:
        frame = picam.capture_array()
        # detectamos el patrón
        desbloqueado = detector.detectar_patron(patron, not_patron, picam)
    
    # esperamos 3 segundos y pasamos a la siguiente fase
    cv2.waitKey(5000)

    # 2) Dibujar el patron de la pantalla
    disney_tracker.initialize_tracker(picam)
    cv2.destroyAllWindows()

    picam.stop()
    

