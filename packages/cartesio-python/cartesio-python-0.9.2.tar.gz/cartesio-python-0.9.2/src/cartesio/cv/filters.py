import cv2
import numpy as np

from cartesio.model.function import FunctionNode
from cartesio.cv.kernels import correct_ksize, SHARPEN_KERNEL, kernel_from_parameters, ROBERT_CROSS_H_KERNEL, ROBERT_CROSS_V_KERNEL
from skimage.data import cell
from scipy.stats import kurtosis, skew


class MedianBlur(FunctionNode):
    def __init__(self):
        super(MedianBlur, self).__init__('median_blur', 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.medianBlur(connections[0], ksize)


class GaussianBlur(FunctionNode):
    def __init__(self):
        super(GaussianBlur, self).__init__('gaussian_blur', 1, 1)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        return cv2.GaussianBlur(connections[0], (ksize, ksize), 0)


class Laplacian(FunctionNode):
    def __init__(self):
        super(Laplacian, self).__init__('laplacian', 1, 0)

    def __call__(self, connections, parameters):
        return cv2.Laplacian(connections[0], cv2.CV_64F).astype(np.uint8)


class Sobel(FunctionNode):
    def __init__(self):
        super().__init__('sobel', 1, 2)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        if parameters[1] < 128:
            return cv2.Sobel(connections[0], cv2.CV_64F, 1, 0, ksize=ksize).astype(np.uint8)
        return cv2.Sobel(connections[0], cv2.CV_64F, 0, 1, ksize=ksize).astype(np.uint8)


class RobertCross(FunctionNode):
    def __init__(self):
        super().__init__('robert_cross', 1, 1)

    def __call__(self, connections, parameters):
        img = (connections[0] / 255.).astype(np.float32)
        h = cv2.filter2D(img, -1, ROBERT_CROSS_H_KERNEL)
        v = cv2.filter2D(img, -1, ROBERT_CROSS_V_KERNEL)
        return (cv2.sqrt(cv2.pow(h, 2) + cv2.pow(v, 2)) * 255).astype(np.uint8)


class Canny(FunctionNode):
    def __init__(self):
        super(Canny, self).__init__('canny', 1, 2)

    def __call__(self, connections, parameters):
        return cv2.Canny(connections[0], parameters[0], parameters[1])


class Sharpen(FunctionNode):
    def __init__(self):
        super().__init__('sharpen', 1, 0)

    def __call__(self, connections, parameters):
        return cv2.filter2D(connections[0], -1, SHARPEN_KERNEL)


class AbsoluteDifference(FunctionNode):
    def __init__(self):
        super().__init__('abs_diff', 1, 2)

    def __call__(self, connections, parameters):
        ksize = correct_ksize(parameters[0])
        image = connections[0].copy()
        return image - cv2.GaussianBlur(image, (ksize, ksize), 0) + parameters[1]


class FluoTopHat(FunctionNode):
    def __init__(self):
        super().__init__('fluo_tophat', 1, 2)

    def rescale_intensity(self, img, min_val, max_val):
        output_img = np.clip(img, min_val, max_val)
        output_img = (output_img - min_val) / (max_val - min_val) * 255
        return output_img.astype(np.uint8)

    def __call__(self, connections, p):
        kernel = kernel_from_parameters(p)
        img = cv2.morphologyEx(connections[0], cv2.MORPH_TOPHAT, kernel, iterations=10)
        kur = np.mean(kurtosis(img, fisher=True))
        skew1 = np.mean(skew(img))
        if kur > 1 and skew1 > 1:
            p2, p98 = np.percentile(img, (15, 99.5), interpolation="linear")
        else:
            p2, p98 = np.percentile(img, (15, 100), interpolation="linear")

        return self.rescale_intensity(img, p2, p98)


class RelativeDifference(FunctionNode):
    def __init__(self):
        super().__init__('rel_diff', 1, 1)

    def __call__(self, connections, p):
        img = connections[0]
        max_img = np.max(img)
        min_img = np.min(img)

        ksize = correct_ksize(p[0])
        gb = cv2.GaussianBlur(img, (ksize, ksize), 0)
        gb = np.float32(gb)

        img = np.divide(img, gb + 1e-15, dtype=np.float32)
        img = cv2.normalize(img, img, max_img, min_img, cv2.NORM_MINMAX)
        return img.astype(np.uint8)
