import os
from pathlib import Path
import argparse
import cv2
import numpy as np
from tqdm import tqdm

from src.utils.image_utils import relabel_image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Divide data into patches")
    parser.add_argument(
        '--masks',
        type=str,
        default="C:/Users/Julia/Downloads/outputs/outputs/",
        help='Folder with images'
    )
    parser.add_argument(
        '--masks_gt',
        type=str,
        default="F:/Cell Detection Visual Data/Data/BCCD Dataset with mask/test/mask/",
        help='Folder with masks'
    )
    parser.add_argument(
        '--res',
        type=str,
        default="C:/Users/Julia/Downloads/outputs/outputs/res/",
        help='Directory for extracted_patches, two dirs: masks and images will be created'
    )

    args = parser.parse_args()

    res_folder = os.path.join(args.res, "masks")
    os.makedirs(res_folder, exist_ok=True)

    gt_paths = sorted(Path(args.masks_gt).glob('*.*'))
    masks_paths = sorted(Path(args.masks).glob('*.*'))

    for gt_path, mask_path in tqdm(zip(gt_paths, masks_paths), total=len(gt_paths), desc="Processing"):
        gt = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        h, w = mask.shape
        new_mask = np.zeros_like(gt)
        new_mask[:h, :w] = mask
        new_mask = relabel_image(new_mask)

        img_name = os.path.splitext(os.path.basename(gt_path))[0]
        name_patch = f"{img_name}.npy"
        np.save(os.path.join(res_folder, name_patch), new_mask)