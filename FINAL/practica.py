import detector 
import cv2
import calibration
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
    patron, not_patron = detector.obtener_patrones()

    desbloqueado = False

    while not desbloqueado:
        frame = picam.capture_array()
        # detectamos el patrón
        desbloqueado = detector.detectar_patron(patron, not_patron, picam)
    
    # esperamos 3 segundos y paramos la grabación
    cv2.waitKey(3000)
    picam.stop()
    

