# -*- coding:utf-8 -*-

# bfscore: Contour/Boundary matching score for multi-class image segmentation #
# Reference: Csurka, G., D. Larlus, and F. Perronnin. "What is a good evaluation measure for semantic segmentation?" Proceedings of the British Machine Vision Conference, 2013, pp. 32.1-32.11. #
# Crosscheck: https://www.mathworks.com/help/images/ref/bfscore.html #

import cv2
import numpy as np
import math

major = cv2.__version__.split('.')[0]  # Get opencv version
bDebug = False

""" For precision, contours_a==GT & contours_b==Prediction
    For recall, contours_a==Prediction & contours_b==GT """


def calc_precision_recall(contours_a, contours_b, threshold):
    x = contours_a
    y = contours_b

    xx = np.array(x)
    hits = []
    for yrec in y:
        d = np.square(xx[:, 0] - yrec[0]) + np.square(xx[:, 1] - yrec[1])
        hits.append(np.any(d < threshold * threshold))
    top_count = np.sum(hits)

    try:
        precision_recall = top_count / len(y)
    except ZeroDivisionError:
        precision_recall = 0

    return precision_recall, top_count, len(y)


""" computes the BF (Boundary F1) contour matching score between the predicted and GT segmentation """


def bfscore(gt_, pr_, threshold=2):
    gt_[gt_ > 0] = 1
    pr_[pr_ > 0] = 1
    gt_ = gt_.astype(np.uint8)
    pr_ = pr_.astype(np.uint8)
    classes_gt = np.unique(gt_)  # Get GT classes
    classes_pr = np.unique(pr_)  # Get predicted classes

    # Check classes from GT and prediction
    if not np.array_equiv(classes_gt, classes_pr):
        print('Classes are not same! GT:', classes_gt, 'Pred:', classes_pr)

        classes = np.concatenate((classes_gt, classes_pr))
        classes = np.unique(classes)
        classes = np.sort(classes)
    else:
        classes = classes_gt  # Get matched classes

    m = np.max(classes)  # Get max of classes (number of classes)
    # Define bfscore variable (initialized with zeros)
    bfscores = np.zeros((m + 1), dtype=float)
    areas_gt = np.zeros((m + 1), dtype=float)

    for i in range(m + 1):
        bfscores[i] = np.nan
        areas_gt[i] = np.nan

    for target_class in classes:  # Iterate over classes

        if target_class == 0:  # Skip background
            continue

        gt = gt_.copy()
        gt[gt != target_class] = 0
        contours, _ = cv2.findContours(gt, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contours_gt = []
        for i in range(len(contours)):
            for j in range(len(contours[i])):
                contours_gt.append(contours[i][j][0].tolist())
        if bDebug:
            print('contours_gt')
            print(contours_gt)

        # Get contour area of GT
        if contours_gt:
            area = cv2.contourArea(np.array(contours_gt))
            areas_gt[target_class] = area

        # Draw GT contours
        size = gt_.shape
        img = np.zeros((size[0], size[1], 3), dtype=np.uint8)
        img[gt == target_class, 0] = 128  # Blue
        img = cv2.drawContours(img, contours, -1, (255, 0, 0), 1)

        pr = pr_.copy()
        pr[pr != target_class] = 0

        contours, _ = cv2.findContours(pr, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contours_pr = []
        for i in range(len(contours)):
            for j in range(len(contours[i])):
                contours_pr.append(contours[i][j][0].tolist())

        # Draw predicted contours
        img[pr == target_class, 2] = 128  # Red
        img = cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

        # 3. calculate
        precision, numerator, denominator = calc_precision_recall(
            contours_gt, contours_pr, threshold)  # Precision

        recall, numerator, denominator = calc_precision_recall(
            contours_pr, contours_gt, threshold)  # Recall

        try:
            f1 = 2 * recall * precision / (recall + precision)  # F1 score
        except:
            f1 = np.nan

        bfscores[target_class] = f1

    return bfscores[1:], areas_gt[1:], img  # Return bfscores, except for background


if __name__ == "__main__":

    sample_gt = 'data/gt_1.png'
    # sample_gt = 'data/gt_0.png'

    sample_pred = 'data/crf_1.png'
    # sample_pred = 'data/pred_0.png'

    score, areas_gt = bfscore(sample_gt, sample_pred, 2)  # Same classes
    # score, areas_gt = bfscore(sample_gt, sample_pred, 2)    # Different classes

    # gt_shape = cv2.imread('data/gt_1.png').shape
    # print("Total area:", gt_shape[0] * gt_shape[1])

    total_area = np.nansum(areas_gt)
    print("GT area (except background):", total_area)
    fw_bfscore = []
    for each in zip(score, areas_gt):
        if math.isnan(each[0]) or math.isnan(each[1]):
            fw_bfscore.append(math.nan)
        else:
            fw_bfscore.append(each[0] * each[1])
    print(fw_bfscore)

    print("\n>>>>BFscore:\n")
    print("BFSCORE:", score)
    print("Per image BFscore:", np.nanmean(score))

    print("\n>>>>Weighted BFscore:\n")
    print("Weighted-BFSCORE:", fw_bfscore)
    print("Per image Weighted-BFscore:", np.nansum(fw_bfscore) / total_area)
