import os
import argparse

from src.metrics.plots import save_plots
from src.metrics.stats import save_prediction_visualization, run_nuclei_inst_stat

"""
Author: Julia Merta
Date: 02-01-2025

Info: 

      You can run this script from the command line (read the parameters info below).
      Another way is to set the correct paths and options here in the code and run.
      
      This script can be used to evaluate the performance of your method. 
      First you have to set the directories where you saved your predictions and ground truth 
      masks. Both of them need to be saved as .npy arrays of two dimensions. Each nucleus
      in both GT and prediction masks need to have ist own number. It means that when you
      have two instances of nucleus in a mask the first instance will have all elements set to 1
      and the second instance will have all elements set to 2 (bg pixels will be 0).
      
      You can try to prepare masks using relabel_image function from utils.image_utils.relabel_image()
      
      img = np.load(filename) or cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
      mask = relabel_image(image)
      np.save(res_filename, mask) # that will convert the mask to the correct format
      
      1. Statistics calculation
      
      Following segmentation statistics would be calculated:
      - DICE
      - AJI
      - AJI+ (another variant of AJI)
      - Boundary F1 score
      - PQ
      
      Following instance detection statistics would be calculated:
      - Recall -  under IoU=0.5
      - Precision -  under IoU=0.5
      - F1 -  under IoU=0.5
      - FDR -  under IoU=0.5
      
      Statistics for each image would be saved to the stats.csv file.
      Summary segmentation statistics for the whole dataset would be saved to summary.csv 
      Summary detection statistics for the whole dataset would be saved to summary_detection.csv 
      
      For Boundary F1 score the visualization results will be saved to the stats/bf_vis folder
      
      In this step plots created for obtained statistics will be saved to the /plots folder.
      
      2. Visualization results
      
      In this step for each mask the .png file with visualization of TP, FP and FN pixels will be created.
      Results will be saved to the visualization_masks folder.
      
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Divide data into patches")
    parser.add_argument(
        '--gt',
        type=str,
        default="example_data/numpy_gt",
        help='Folder with masks'
    )
    parser.add_argument(
        '--pred',
        type=str,
        default="example_data/numpy_pred",
        help='Directory for extracted_patches, two dirs: masks and images will be created'
    )
    parser.add_argument(
        '--res',
        type=str,
        default="example_data/res",
        help='Folder for the results'
    )
    parser.add_argument(
        '--actions',
        nargs='*',
        choices=[
            'Segmentation stats',  # DICE, AJI, PQ, AJI+, BF score, Recall, Precision, F1 and FDR
                                   # per image and per dataset
            'Visualisation',  # save masks with results visualization (pixel level)
        ],
        default=[
            'Segmentation stats',
            'Visualisation',
        ],
        help="Steps to perform. If you want to omit some steps, just remove them from the"
             "default list."
    )

    args = parser.parse_args()

    if "Segmentation stats" in args.actions:
        dir_stats = os.path.join(args.res, "stats")
        os.makedirs(dir_stats, exist_ok=True)
        dir_bf = os.path.join(dir_stats, "bf_vis")
        os.makedirs(dir_bf, exist_ok=True)
        df_stats, df_summary, df_detection = run_nuclei_inst_stat(args.gt, args.pred, dir_bf)
        df_stats.to_csv(os.path.join(dir_stats, "stats.csv"), index=False)
        df_summary.to_csv(os.path.join(dir_stats, "summary.csv"), index=True)
        df_detection.to_csv(os.path.join(dir_stats, "summary_detection.csv"), index=False)
        dir_viz = os.path.join(args.res, "plots")
        os.makedirs(dir_viz, exist_ok=True)
        save_plots(df_stats, dir_viz)
    if "Visualisation" in args.actions:
        dir_viz = os.path.join(args.res, "visualization_masks")
        os.makedirs(dir_viz, exist_ok=True)
        save_prediction_visualization(args.gt, args.pred, dir_viz)
