# Proyecto: Detector de Canicas en una Carrera
 
Este proyecto utiliza una Raspberry Pi con la cámara Module 3 para detectar y clasificar canicas en una carrera según sus colores. La Raspberry Pi captura imágenes de la pista de carrera, procesa las imágenes para identificar las canicas de diferentes colores y determina la canica ganadora según la primera en cruzar la línea de fin.
 
## Materiales Necesarios
 
1. Raspberry Pi con cámara Module 3.
2. Pista de carrera para canicas con una línea de fin.
3. Canicas de colores diferentes.
 
## Configuración del Proyecto
 
1. **Instalación de Bibliotecas:**
   - Instala las bibliotecas necesarias en tu Raspberry Pi ejecutando el siguiente comando en la terminal:
     ```bash
     pip install opencv-python
     ```
 
2. **Configuración de Hardware:**
   - Coloca la Raspberry Pi en un lugar donde tenga una buena vista de la pista de carrera. Asegúrate de que la cámara esté apuntando hacia la línea de fin.
 
3. **Ejecución del Programa:**
   - Ejecuta el programa principal (`main.py`) para comenzar la captura de imágenes y el procesamiento.
 
## Estructura del Proyecto
 
- **`main.py`:** El programa principal que realiza la captura de imágenes, procesamiento y determina la canica ganadora.
- **`utils.py`:** Módulo de utilidades que contiene funciones auxiliares para el procesamiento de imágenes.
- **`README.md`:** Este archivo que proporciona información detallada sobre el proyecto.
 
## Ejecución del Proyecto
 
```bash
python main.py
 
