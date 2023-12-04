import detector 
import cv2
import calibration
import dibujar 
import formas
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

    # 0) Iniciar video de salida
    output_file = "output_video.mp4"
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 30
    output_video = cv2.VideoWriter(output_file, codec, fps, (640, 480))

    # 1) Detectar la secuencia de patrones
    patron, not_patron = detector.obtener_patrones()
    desbloqueado = False

    while not desbloqueado:
        frame = picam.capture_array()
        # detectamos el patrón
        desbloqueado = detector.detectar_patron(patron, not_patron, picam, output_video)
    
    # esperamos 5 segundos y pasamos a la siguiente fase
    cv2.waitKey(5000)

    salir = False
    while not salir:

        # 2) Detectar la forma que se va a querer seguir
        forma, salir = formas.tracker_objetos(picam, output_video)

        # 3) Procedemos a dibujar la forma pedida
        if forma != None:
            salir = dibujar.complete_figure(forma, picam, output_video)

    output_video.release()
    cv2.destroyAllWindows()

    picam.stop()


