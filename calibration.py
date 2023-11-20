import numpy as np
import cv2
import imageio
import matplotlib.pyplot as plt



# cargamos las imagenes:
def load_images(filenames):
    return [imageio.imread(filename) for filename in filenames]

def find_centers(images):
    centers = []
    rets = []
    for image in images:
        # como nuestro patron son circulos 4x6 tenemos que buscar los centros
        # de los circulos
        ret, corners = cv2.findCirclesGrid(image, (4, 6), None)
        centers.append(corners)
        rets.append(ret)
    return centers, rets

def show_centers(images, centers, rets):
    # mostramos una matriz de 5x2 con las imagenes y los centros
    # de los circulos
    images2 = deepcopy(images)
    for i, image in enumerate(images2):
        cv2.drawChessboardCorners(image, (4, 6), centers[i], rets[i])
    
    # now we show the images
    plt.figure(figsize=(15, 15))
    for i, image in enumerate(images2):
        plt.subplot(5, 2, i+1)
        plt.imshow(image)
        plt.axis('off')
    plt.show()

    return images2


def get_circle_centers(patron_shape, dx, dy):
    # patron_shape: (4, 6)
    # dx, dy: distancia entre centros
    points = []
    for i in range(patron_shape[0]):
        for j in range(patron_shape[1]):
            points.append([dx*i, dy*j])
    return np.array(points, dtype=np.float32)

if __name__ == '__main__':

    filenames = ['center/center_{:03d}.jpg'.format(i) for i in range(10)]

    images = load_images(filenames)

    centers, rets = find_centers(images)

    # visualize the centers
    images2 = show_centers(images, centers, rets)

    # obtain the centers of the circles
    real_points = get_circle_centers((4, 6), 1, 1)

    # now we calibrate the camera
    # we need to obtain the camera matrix and the distortion coefficients
    # we use the function cv2.calibrateCamera
    valid_centers = [centers[i] for i in range(len(rets)) if rets[i]]
    num_valid_images = len(valid_centers)
    # obtain their real points
    real_points = np.asarray([real_points for i in range(num_valid_images)], dtype=np.float32)

    # convert the corners list to array
    image_points = np.asarray(valid_centers, dtype=np.float32)

    # now we calibrate the camera
    rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(real_points, image_points, images[0].shape[:2], None, None)

    extrinsics = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))

    print('Calibration matrix:')
    print('-------------------')
    print('Intrinsic parameters:')
    print(intrinsics+'\n')
    print('Distortion coefficients:')
    print(dist_coeffs+'\n')
    print('Extrinsic parameters:')
    print(extrinsics+'\n')
    print('RMS:')
    print(rms+'\n')


