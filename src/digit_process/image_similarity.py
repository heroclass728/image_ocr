import numpy as np
import cv2

from skimage.metrics import structural_similarity as ssim


def compare_two_images(test_frame, origin_frame):

    # compute the mean squared error and structural similarity
    # index for the images
    test_frame = cv2.resize(test_frame, (origin_frame.shape[1], origin_frame.shape[0]))
    m = mse(test_frame, origin_frame)
    s = ssim(test_frame, origin_frame, multichannel=True)

    return m, s


def mse(image_a, image_b):

    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are

    return err


if __name__ == '__main__':

    compare_two_images(test_frame_path="", origin_frame_path="")
