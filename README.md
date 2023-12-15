# Practica Final Vision
### Hecho por Lara Ocón y Lucía Prado



https://github.com/lara-ocon/PracticaFinalVision/assets/112928240/61926bd7-c5aa-4b51-8c9d-95f13924a4db

El alcance de la práctica abarca varias etapas fundamentales en el procesamiento de imágenes y visión por computadora. En primer lugar, se lleva a cabo una calibración (***calibration.py***) efectiva de la cámara para obtener sus parámetros intrínsecos y extrínsecos empleando imágenes de un patrón compuesto por 5x4 círculos. 

Posteriormente, se implementa la detección patrones mediante SIFT (***detector.py***), que más tarde emplearemos para la ejecución del decodificador de secuencia. Dicho decodificador memoriza la cantidad de patrones consecutivos que desee el usuario y garantiza el paso al siguiente bloque si dicha secuencia se introduce correctamente. En caso de mostrar una carta incorrecta o desordenada, el proceso se reinicia.
Una vez superada la etapa de detección de secuencia, se introduce un módulo que emplea trackers para detectar y seguir figuras con colores específicos (***formas.py***). El usuario debe seleccionar la forma a mostrar por pantalla, que determinará la figura que el usuario deberá dibujar en la fase final de la práctica (***dibujar.py***). Al finalizar la trayectoria de dicha figura mostrada por pantalla, se calcula la similitud entre la figura mostrada y la dibujada para evaluar el rendimiento del usuario.

Todos estos modulos son incorporados por uno solo en el cual se ejecutan las distintas fases secuencialmente, y se guarda la salida en un archivo mp4 (***practica.py***).
