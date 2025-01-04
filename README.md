# Script to evaluate segmentation results

Following segmentation statistics would be calculated:
- DICE
- AJI
- AJI+ (another variant of AJI)
- PQ
- Boundary F1 score
      
Following instance detection statistics would be calculated:
- Recall -  under IoU=0.5
- Precision -  under IoU=0.5
- F1 -  under IoU=0.5
- FDR -  under IoU=0.5

---

## Requirements

To install all the required dependencies, use the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

# How to Use the Script

1. Prepare Your Data

You will need:
- Prediction masks saved in one folder.
- Ground truth (GT) masks saved in another folder.

File requirements:
- The filenames of corresponding masks in both folders should match exactly.
- For example: mask_1.npy in both GT and prediction folders.
- The masks must be saved as NumPy arrays (.npy files).
- Each nucleus in the mask must have a unique ID. So if you have two nuclei in the mask, one will be filled with values 1 and the second with values 2. Background should be filled with 0.

2. Configure the Script
- Open the file: src/calculate_stats.py.
- Set the paths to your directories containing the prediction masks and ground truth masks.

3. Execute the script:

```python
python src/calculate_stats.py
```
- The script will process the data and save results, including plots and evaluation metrics. More details about the output files can be found in the comments within calculate_stats.py.

4. Try the Demo
- A folder named example_data contains demo masks for testing.
- Run the script with its default settings to generate example plots and results for reference.

5. Script to extract patches
- I provided a script to divide images into patches. You have to set paths to directories and run the script. Masks will be relabeled in a way that was mentioned before.  

7. References
- implementation of Boundary F1 score
https://github.com/minar09/bfscore_python
- implementation of DICE, AJI, AJI+ and PQ is based on:
@article{graham2019hover,
  title={Hover-net: Simultaneous segmentation and classification of nuclei in multi-tissue histology images},
  author={Graham, Simon and Vu, Quoc Dang and Raza, Shan E Ahmed and Azam, Ayesha and Tsang, Yee Wah and Kwak, Jin Tae and Rajpoot, Nasir},
  journal={Medical Image Analysis},
  pages={101563},
  year={2019},
  publisher={Elsevier}
}
