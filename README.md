# Script to evaluate segmentation results

The following segmentation statistics are available:
- DICE
- AJI
- AJI+ (another variant of AJI)
- PQ
- Boundary F1 score
      
The following instance detection statistics are available:
- Recall -  for the threshold IoU=0.5 
- Precision -  for the threshold IoU=0.5 
- F1 -  for the threshold IoU=0.5 
- FDR -  for the threshold IoU=0.5 

---

## Requirements

To install all the required dependencies, use the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

# How to Use the Script

## 1. Prepare Your Data

### You will need:
- Prediction masks saved in one folder.
- Ground truth (GT) masks saved in another folder.

### File requirements:
- The filenames of corresponding masks in both folders should match exactly. For example: `mask_1.npy` in both GT and prediction folders.
- The masks must be saved as NumPy arrays (`.npy` files).
- Each nucleus in the mask must have a unique ID. So if you have two nuclei in the mask, one will be filled with values 1 and the second with values 2. The background should be filled with 0.

## 2. Configure the Script
- Open the file: `src/calculate_stats.py`.
- Set the paths to your directories containing the prediction masks and ground truth masks.

## 3. Execute the script:

```python
python src/calculate_stats.py
```
- The script will process the data and save results, including plots and evaluation metrics. More details about the output files can be found in the comments within `calculate_stats.py`.

## 4. Results

When the script is executed, three new folders will be created in the main results folder:

### 1. **`stats` folder**  
This folder contains the following files:
- **`bf_vis/`**  
  A subfolder containing visualizations of the Boundary F1 score for each image.
- **`stats.csv`**  
  A CSV file with statistics calculated for each image, including:
  - DICE  
  - AJI  
  - AJI+  
  - PQ  
  - Boundary F1 score  
  - Recall  
  - Precision  
  - F1  
  - FDR  
  - True Positives  
  - False Positives  
  - False Negatives
- **`summary.csv`**  
  A file summarizing detection statistics, including the **average**, **standard deviation**, and **median** of:
  - DICE  
  - AJI  
  - AJI+  
  - PQ  
  - Boundary F1 score (for all images)
- **`summary_detection.csv`**  
  A file containing **Recall**, **Precision**, **F1**, and **FDR** calculated based on the accumulated **True Positives**, **False Positives**, and **False Negatives**.

---

### 2. **`vizualization_masks` folder**  
This folder contains pixel-level visualizations of results for each image:
- **Green pixels**: True Positives (TP)  
- **Blue pixels**: False Negatives (FN)  
- **Red pixels**: False Positives (FP)

---

### 3. **`plots` folder**  
This folder contains violin plots generated based on data from the `stats.csv` file.

## 5. Try the Demo
- A folder named example_data contains demo masks for testing.
- Run the script with its default settings to generate example plots and results for reference.

## 6. Script to extract patches
- A script `prepare_patches.py` can be used to divide images into patches. You have to set paths to directories and run the script. Masks will be relabeled in a way that was mentioned before.
  
## References

1. **Implementation of Boundary F1 Score**  
   - [bfscore_python GitHub Repository](https://github.com/minar09/bfscore_python)

2. **Implementation of DICE, AJI, AJI+, and PQ** is based on:  

   - Graham, Simon, Vu, Quoc Dang, Raza, Shan E Ahmed, Azam, Ayesha, Tsang, Yee Wah, Kwak, Jin Tae, and Rajpoot, Nasir.  
     *Hover-net: Simultaneous segmentation and classification of nuclei in multi-tissue histology images.*  
     **Medical Image Analysis**, Elsevier, 2019. Pages: 101563.  
     DOI: [10.1016/j.media.2019.101563](https://doi.org/10.1016/j.media.2019.101563)
