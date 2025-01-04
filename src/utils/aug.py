import random
import cv2
import numpy as np


def random_flip_rotate(img, mask):
    assert img.ndim >= mask.ndim
    axes = tuple(range(mask.ndim))
    perm = tuple(np.random.permutation(axes))
    img = img.transpose(perm + tuple(range(mask.ndim, img.ndim)))
    mask = mask.transpose(perm)
    for ax in axes:
        if np.random.rand() > 0.5:
            img = np.flip(img, axis=ax)
            mask = np.flip(mask, axis=ax)
    return img, mask


def gaussian_blur(img, val=[3, 5, 7], sigma_range=(0.1, 2)):
    ksize = random.choice(val)
    sigma = random.uniform(*sigma_range)
    return cv2.GaussianBlur(img, (ksize, ksize), sigma)


def avg_blur(img, val=[3, 5, 7]):
    ksize = random.choice(val)
    return cv2.blur(img, (ksize, ksize))


def add_to_saturation(img, alpha_range=(0.5, 1.1), beta_range=(0.5, 1.1)):
    alpha = random.uniform(*alpha_range)
    beta = random.uniform(*beta_range)
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return img


def add_to_intensity(img, val_range=(-30, 30)):
    img = np.clip(img + random.randint(*val_range), 0, 255)
    return img


def random_blur(img, prob=0.5):
    functions = [gaussian_blur, avg_blur]
    if random.random() < prob:
        aug = random.choice(functions)
        img = aug(img)
    return img


def random_color_augment(img, prob=0.5):
    functions = [add_to_saturation]
    if random.random() < prob:
        aug = random.choice(functions)
        img = aug(img)
    return img


def augmenter(x, y):
    x, y = random_flip_rotate(x, y)
    x = random_blur(x)
    x = random_color_augment(x)
    x = x / 255.0
    return x, y


def normalize(x, y):
    x = x / 255.0
    return x, y
