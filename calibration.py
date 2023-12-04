import numpy as np
import cv2
import imageio
import matplotlib.pyplot as plt
# importamos deepcopy para copiar objetos
from copy import deepcopy

# cargamos las imagenes:
def load_images(filenames):
    return [imageio.imread(filename) for filename in filenames]

def find_centers(images):
    centers = [cv2.findCirclesGrid(image, (5, 4), None) for image in images]

    return centers

def show_centers(images, centers):
    # mostramos una matriz con las 23 imagenes y los centros encontrados
    images2 = deepcopy(images)
    tmp = [cv2.drawChessboardCorners(img, (5,4), cor[1], cor[0]) for img, cor in zip(images2, centers) if cor[0]]
    # now we show the images in a matrix, 4x6
    fig, ax = plt.subplots(4, 6, figsize=(20, 10))
    for i, image in enumerate(images2):
        ax[i//6, i%6].imshow(image)
        ax[i//6, i%6].axis('off')
        # ponemos el numero de la imagen
        ax[i//6, i%6].set_title(f'Image {i+1}')
    plt.show()
    return images2


def get_circle_centers(chessboard_shape, dx, dy):
    return [[(i%chessboard_shape[0])*dx, (i//chessboard_shape[0])*dy, 0] for i in range(np.prod(chessboard_shape))]


def calibrate():
    
    # cargamos las imagenes
    filenames = [f'calibracion/img{i}.jpg' for i in range(1,24)]
    images = load_images(filenames)

    centers = find_centers(images)

    images2 = show_centers(images, centers)

    # centers:
    valid_centers = [cor[1] for cor in centers if cor[0]]
    num_valid_images = len(valid_centers)

    # obtain their real points
    real_points = get_circle_centers((5, 4), 20, 20)
    real_points = np.asarray([real_points for i in range(num_valid_images)], dtype=np.float32)

    # We are going to convert our coordinates list in the reference system to numpy array
    object_points = np.asarray([real_points for i in range(num_valid_images)], dtype=np.float32)

    # convert the corners list to array
    image_points = np.asarray(valid_centers, dtype=np.float32)

    # now we calibrate the camera
    rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(real_points, image_points, images[0].shape[:2], None, None)

    extrinsics = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))

    print('Calibration matrix:')
    print('-------------------')
    print('Intrinsic parameters:')
    print(intrinsics, '\n')
    print('Distortion coefficients:')
    print(dist_coeffs, '\n')
    # print('Extrinsic parameters:')
    # print(extrinsics, '\n')
    print('RMS:')
    print(rms, '\n')


if __name__ == '__main__':
    calibrate()
