import os
from pathlib import Path
import argparse
import cv2
from tqdm import tqdm

from src.utils.image_utils import relabel_image

"""
Author: Julia Merta
Date: 31-12-2024

Info: 
      
      You can run this script from the command line (read the parameters info below).
      Another way is to set the correct paths and options here in the code and run.
      Patches will be saved to the chosen directory (images and masks), they will be 
      converted to .png image format. To the name of each patch the information about
      the localization in the image will be added (for instance patch_100_200_256_256.png 
      is the patch which has its upper left corner at position (100, 200) and has the
      256 pixels in width and 256 pixels in height). 
      
      When mode cut is selected, when the image size is not divisible by the patch size,
      to small patches will be discarded (we will lose some information). When the mode 
      overlap is selected to small patches will be extended by overlapping the previous 
      patches (introducing some data redundancy). 
      
      If you want to reduce the image size before the division set scale parameter.
      The coordinates of the patches will be assigned according to the scaled image.
      
      When relabel parameter is set to True, each patch will have different pixel intensity
      according to the number of cell in the image (1, 2, 3 .... n) - it can be useful for
      some deep learning models.
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Divide data into patches")
    parser.add_argument(
        '--images',
        type=str,
        default="F:/Cell Detection Visual Data/Data/BCCD Dataset with mask/train/original/",
        help='Folder with images'
    )
    parser.add_argument(
        '--masks',
        type=str,
        default="F:/Cell Detection Visual Data/Data/BCCD Dataset with mask/train/mask/",
        help='Folder with masks'
    )
    parser.add_argument(
        '--patches_folder',
        type=str,
        default="F:/Cell Detection Visual Data/Data/BCCD Dataset with mask/train/patches/",
        help='Directory for extracted_patches, two dirs: masks and images will be created'
    )
    parser.add_argument(
        '--size',
        type=int,
        default=256,
        help='Size of the patch'
    )
    parser.add_argument(
        '--extract_mode',
        type=str,
        default="overlap",
        help='overlap - when we have patches in the border with incorrect size we take some pixels from '
             'the previous patch '
             'cut - when we have patches in the border we extract only patches with correct size'
    )
    parser.add_argument(
        '--relabel_images',
        type=bool,
        default=True,
        help='Relabel images or not'
    )

    args = parser.parse_args()

    masks_folder = os.path.join(args.patches_folder, "masks")
    images_folder = os.path.join(args.patches_folder, "images")
    os.makedirs(masks_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)

    img_paths = sorted(Path(args.images).glob('*.*'))
    masks_paths = sorted(Path(args.masks).glob('*.*'))
    tile_size = args.size

    for img_path, mask_path in tqdm(zip(img_paths, masks_paths), total=len(img_paths), desc="Processing"):
        img = cv2.imread(img_path, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        h, w, d = img.shape

        if args.extract_mode == 'overlap':
            if h % args.size != 0:
                h = h+args.size - h % args.size
            if w % args.size != 0:
                w = w + args.size - w % args.size

        for y in range(0, h, args.size):
            for x in range(0, w, args.size):

                patch_img = img[y:y + args.size, x:x + args.size]
                patch_mask = mask[y:y + args.size, x:x + args.size]
                h_patch, w_patch, _ = patch_img.shape

                if h_patch != args.size or w_patch != args.size:
                    diff_h = args.size - h_patch
                    diff_w = args.size - w_patch
                    patch_img = img[y - diff_h:y + args.size, x - diff_w:x + args.size]
                    patch_mask = mask[y - diff_h:y + args.size, x - diff_w:x + args.size]

                if args.relabel_images:
                    patch_mask = relabel_image(patch_mask)

                img_name = os.path.splitext(os.path.basename(img_path))[0]
                name_patch = f"{img_name}_{y}_{x}_{args.size}_{args.size}.png"

                cv2.imwrite(os.path.join(images_folder, name_patch), patch_img)
                cv2.imwrite(os.path.join(masks_folder, name_patch), patch_mask)
