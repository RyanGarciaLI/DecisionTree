# DecisionTree
A decision tree implemented by Hunt's Algorithm.

Author SIDs:  
- An LYU: 1155124488
- Dongsheng YUAN: 1155177815
- Jianhui GE: 1155107776
- Xiang WU: 1155124573
- Yuxin LI: 1155107874

## Dataset
- Original Dataset is available at http://archive.ics.uci.edu/ml/datasets/Adult
- The Training Dataset is located at the directory "/DecisionTree/rawData/"
- The Test Dataset is located at the directory "/DecisionTree/rawData/"

## Usage
You can run the script with the following command:

    ```
    python main.py <data_path_train> <data_path_test> [options ...]
    ```
* `<data_path_train>`: The path of the training dataset, which is set as "./rawData/adult.data" by default.
* `<data_path_test>`: The path of the test dataset, which is set as "./rawData/adult.test" by default.
### Options include:
* `-c <cut_thred>`: The cut threshold is an positive integer limiting the minimum size of dataset in a Decision Tree node while training, i.e. if |S| <= <cut_thred>, then return a leaf node. This parameter is set as 0.0022*<size_of training_set> by default.
* `-o <out_path>`: The output file path where the constructed decision tree will be written. Set as "output.txt" by default.

### Usage Examples:
* `python main.py`
* `python main.py <data_path_train> <data_path_test>`
* `python main.py -c 50`
* `python main.py -o out.txt`
* `python main.py -c 50 -o out.txt`
* `python main.py <data_path_train> <data_path_test> -c 50 -o out.txt`

## File Structure
### Source Codes
- `preproc.py`  The script to preprocess the raw data.
- `DecisionTree.py` The module implementing the Hunt's algorithm for Decision tree; providing useful APIs e.g., fit(), predict().
- `main.py` The point of execution. 

### Output Files
- `<out_path>` The output file where the constructed decision tree is printed.
- `predicted_result.txt` The output file showing the empirical error; and indicating that, for each record in the evaluation set, its attributes and whether it has been classified successfully. 

### Report
- `report.txt` A report describing the decision tree built from the Adult training set, and introducing how to read/understand our output. 



