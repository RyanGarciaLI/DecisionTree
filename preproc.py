import sys
import csv

HEADERS = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
    'relationship', 'race', 'sex', 'capital-gain', 'captial-loss', 'hours-per-week']
ORDINAL = 'ordinal'
NOMINAL = 'nominal'
ATTRI_TYPE = [ORDINAL, NOMINAL, ORDINAL, NOMINAL, ORDINAL, NOMINAL, NOMINAL,
    NOMINAL, NOMINAL, NOMINAL, ORDINAL, ORDINAL, ORDINAL]

MAX_INTEGER = 2147483647

# prevent exceeding field limits.
csv.field_size_limit(MAX_INTEGER)


def read_test_data(path_test):
    """Reads test data from .data file.
    Reads the data record line by line and removes the non-data record and the
    record that contains missing data (i.e., ' ?'). Trims labels by eliminating
    the dot sign '.' at the end.

    Parameters
    ----------
    path_test
        path to test data with the same structure as adult.test

    Returns
    -------
    attributes
        a list of lists of attributes without missing data.
    labels
        a list of labels. e.g., 0 for <= 50K, 1 for >50K
    headers
        a list of attributes' names.
    types
        a list of attribute types, i.e., ordinal or nomial.
    """

    attributes = []
    labels = []
    with open(path_test, newline='') as datafile:
        dataReader = csv.reader(datafile)
        
        # remove first line in test file
        next(dataReader)

        for line in dataReader:
            if len(line) != 15:
                # omit invalid data
                continue

            if ' ?' in line:
                # omit missing data
                continue

            # convert numeric data in str to integer 
            for i in range(len(HEADERS)):
                if ATTRI_TYPE[i] == ORDINAL:
                    line[i] = int(line[i])
                else:
                    line[i] = line[i].strip()

            # remove dot sign from label and represent it in 1 or 0
            label = 0 if line[-1][:-1] == " <=50K" else 1
            labels.append(label)
            # remove 'native-country' attributes
            attributes.append(line[:-2])

    return attributes, labels, HEADERS, ATTRI_TYPE


def read_training_data(path_train):
    """Reads training data from .data file.
    Reads the data record line by line and removes the non-data record and the
    record that contains missing data (i.e., ' ?'). 
    
    Parameters
    ----------
    path_train
        path to training data with the same structure as adult.data
    
    Returns
    -------
    attributes
        a list of lists of attributes without missing data.
    labels
        a list of labels. e.g., 0 for <= 50K, 1 for >50K
    headers
        a list of attributes' names.
    types
        a list of attribute types, i.e., ordinal or nomial.
    """
    attributes = []
    labels = []
    with open(path_train, newline='') as datafile:
        dataReader = csv.reader(datafile)

        for line in dataReader:
            if len(line) != 15:
                # omit invalid data
                continue

            if ' ?' in line:
                # omit missing data
                continue

            # convert numeric data in str to integer 
            for i in range(len(HEADERS)):
                if ATTRI_TYPE[i] == ORDINAL:
                    line[i] = int(line[i])
                else:
                    line[i] = line[i].strip()

            # represent label in terms of 1 or 0
            label = 0 if line[-1] == " <=50K" else 1
            labels.append(label)
            # remove 'native-country' attributes
            attributes.append(line[:-2])

    return attributes, labels, HEADERS, ATTRI_TYPE


