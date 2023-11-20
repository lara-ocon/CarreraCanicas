import cv2
from picamera2 import Picamera2
 
def capturar_y_guardar_imagenes(num_imagenes=10):
    picam = Picamera2()
    picam.preview_configuration.main.size = (640, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
 
    for i in range(num_imagenes):
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        
        nombre_archivo = f"imagen_{i+1}.jpg"
        cv2.imwrite(nombre_archivo, frame)
        print(f"Imagen {i+1} guardada como {nombre_archivo}")
        
        if i < num_imagenes - 1:
            input("Presiona Enter para capturar la siguiente imagen...")
 
    cv2.destroyAllWindows()
    picam.stop()
 
if __name__ == "__main__":
    capturar_y_guardar_imagenes()
