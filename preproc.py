import os
import sys
import csv

DATA_PATH = os.path.join('rawData', 'adult.data')
TEST_PATH = os.path.join('rawData', 'adult.test')
HEADERS = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
    'relationship', 'race', 'sex', 'capital-gain', 'captial-loss', 'hours-per-week']
ORDINAL = 'ordinal'
NOMINAL = 'normial'
ATTRI_TYPE = {
    'age': ORDINAL,
    'workclass' : NOMINAL,
    'fnlwgt' : ORDINAL,
    'education' : NOMINAL, 
    'education-num' : ORDINAL,
    'marital-status' : NOMINAL, 
    'relationship' : NOMINAL,
    'race' : NOMINAL,
    'sex' : NOMINAL,
    'capital-gain' : ORDINAL,
    'captial-loss' : ORDINAL,
    'hours-per-week' : ORDINAL,
}

# prevent exceeding field limits.
csv.field_size_limit(sys.maxsize)


def read_test_data():
    """Reads test data from .data file.

    Reads the data record line by line and removes the non-data record and the
    record that contains missing data (i.e., ' ?'). Trims labels by eliminating
    the dot sign '.' at the end.

    Returns
    -------
    attributes
        a list of lists of attributes without missing data.
    labels
        a list of labels.
    headers
        a list of attributes' names.
    types
        a list of attribute types, i.e., ordinal or nomial.
    """

    attributes = []
    labels = []
    with open(TEST_PATH, newline='') as datafile:
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

            # remove dot sign from label
            label = line[-1][:-1]
            labels.append(label)
            # remove 'native-country' attributes
            attributes.append(line[:-2])

    return attributes, labels, HEADERS, ATTRI_TYPE


def read_training_data():
    """Reads training data from .data file.

    Reads the data record line by line and removes the non-data record and the
    record that contains missing data (i.e., ' ?'). 

    Returns
    -------
    attributes
        a list of lists of attributes without missing data.
    labels
        a list of labels.
    headers
        a list of attributes' names.
    types
        a list of attribute types, i.e., ordinal or nomial.
    """
    attributes = []
    labels = []
    with open(DATA_PATH, newline='') as datafile:
        dataReader = csv.reader(datafile)

        for line in dataReader:
            if len(line) != 15:
                # omit invalid data
                continue

            if ' ?' in line:
                # omit missing data
                continue

            labels.append(line[-1])
            # remove 'native-country' attributes
            attributes.append(line[:-2])

    return attributes, labels, HEADERS, ATTRI_TYPE
    