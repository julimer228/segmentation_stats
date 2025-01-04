import numpy as np
from skimage.measure import label, regionprops


def relabel_image(image):
    label_img = label(image)
    regions = regionprops(label_img)
    output_image = np.zeros_like(label_img, dtype=np.uint8)

    for region in regions:
        if region.area >= 20:
            output_image[label_img == region.label] = region.label
    return output_image


