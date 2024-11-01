"""Numpy"""
import numpy as np


def do_the_thing(padded_image, k_shape, pad, kernel, res):
    """Does the thing!"""
    for i in range(padded_image[pad:-pad, pad:-pad].shape[0]):
        for j in range(padded_image[pad:-pad, pad:-pad].shape[1]):
            # print(f"{kernel.shape} == ({k_shape}, {k_shape})")
            # print(padded_image[i:i + k_shape, j:j + k_shape].shape)
            res[i, j] = np.sum(kernel * padded_image[i:i + k_shape, j:j + k_shape])
    return res


def do_the_thing_color(padded_image, k_shape, pad, kernel, res):
    """Does the thing, but in color!"""
    for i in range(padded_image[pad:-pad, pad:-pad, ...].shape[0]):
        for j in range(padded_image[pad:-pad, pad:-pad, ...].shape[1]):
            for d in range(3):
                res[i, j, d] = np.sum(kernel * padded_image[i:i + k_shape, j:j + k_shape, d])
    return res


def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """ Apply given filter on image """
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2-dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]
    k_shape = kernel.shape[0]
    if k_shape % 2 == 0:
        kernel = np.pad(kernel, (0, 1), mode='constant', constant_values=0)
        k_shape = kernel.shape[0]
    pad = k_shape // 2
    color = image.ndim == 3
    res = np.zeros(image.shape)
    # print(res.shape)
    if color:
        padded_image = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=0)
        # kernel = np.repeat(kernel[:, :, np.newaxis], 3, axis=2)
        res = do_the_thing_color(padded_image, k_shape, pad, kernel, res)

    else:
        padded_image = np.pad(image, ((pad, pad), (pad, pad)), mode='constant', constant_values=0)
        res = do_the_thing(padded_image, k_shape, pad, kernel, res)

    res = np.clip(res, 0, 255).astype(np.uint8)
    return res
