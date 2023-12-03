import cv2
from picamera2 import Picamera2
 
 
def obtener_keypoints_and_descriptors(img):
    sift = cv2.SIFT_create()
    kp, des = sift.detectAndCompute(img, None)
    return kp, des
 
 
def obtener_patrones():
    filenames_patrones = [f'numeros_detector/imagen_{i}.jpg' for i in range(1,11)]
    kp_descriptors = {i: [] for i in range(1,11)}
    for filename, i in zip(filenames_patrones, range(1,11)):
        img = cv2.imread(filename)
        kp, des = obtener_keypoints_and_descriptors(img)
        kp_descriptors[i] = [kp, des]
 
    patron = {i: kp_descriptors[i] for i in range(1,5)}
    not_patron = {i: kp_descriptors[i] for i in range(5, 11)}
 
    return patron, not_patron
 
 
def mostrar_texto(frame, texto):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, texto, (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return frame
 
 
def detectar_patron(patron, not_patron, picam):
    desbloqueado = False
    salir = False
 
    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher()
 
    next_pattern = 1
    current_pattern = 1
 
    while not salir:
        best_match = None
        frame = picam.capture_array()
        kp_frame, des_frame = obtener_keypoints_and_descriptors(frame)
 
        if des_frame is not None:
            for i in range(1,5):
                kp_p, des_p = patron[i]
                matches = bf.knnMatch(des_p, des_frame, k=2)
                good = []
                try:
                    for m, n in matches:
                        if m.distance < 0.7 * n.distance:
                            good.append(m)
                    if len(good) > 20:
                        if best_match is None:
                            best_match = ["patron", i, len(good)]
                        elif best_match[2] < len(good):
                            best_match = ["patron", i, len(good)]
                except:
                    print("error en matches")
 
            for i in range(5, 11):
                kp_np, des_np = not_patron[i]
                matches = bf.knnMatch(des_np, des_frame, k=2)
                good = []
                try:
                    for m, n in matches:
                        if m.distance < 0.7 * n.distance:
                            good.append(m)
                    if len(good) > 20:
                        if best_match is None:
                            best_match = ["not_patron", i, len(good)]
                        elif best_match[2] < len(good):
                            best_match = ["not_patron", i, len(good)]
                except:
                    print("error en matches")
 
            if best_match is not None:
                if best_match[0] == "patron":
                    if best_match[1] == next_pattern:
                        print(f'es el patron que toca con {best_match[2]}')
                        current_pattern = next_pattern
                        next_pattern += 1
                        if next_pattern == 5:
                            print("desbloqueado")
                            desbloqueado = True
                            salir = True
                    elif best_match[1] == current_pattern:
                        print('seguimos en el patron que toca')
                    else:
                        print('el patron es de la secuencia pero no toca')
                        #current_pattern = 0
                        desbloqueado = False
                        salir = True
                elif best_match[0] == "not_patron":
                    print('es un num que no es de la secuencia')
                    frame = mostrar_texto(frame, "No patrón")
                    salir = True
                else:
                    print('no se ha encontrado nada')
                    frame = mostrar_texto(frame, "No se ha encontrado nada")
                    pass
 
        frame = mostrar_texto(frame, "Patrón")
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    return desbloqueado
 
 
if __name__ == "__main__":
    patron, not_patron = obtener_patrones()
 
    picam = Picamera2()
    picam.video_configuration.main.size = (640, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
 
    desbloqueado = False
    while not desbloqueado:
        frame = picam.capture_array()
        desbloqueado = detectar_patron(patron, not_patron, picam)
 
    print('Desbloqueado')
    picam.stop()
