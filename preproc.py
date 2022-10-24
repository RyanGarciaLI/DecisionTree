import sys
import csv


HEADERS = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
    'relationship', 'race', 'sex', 'capital-gain', 'captial-loss', 'hours-per-week']
ORDINAL = 'ordinal'
NOMINAL = 'nominal'
ATTRI_TYPE = [ORDINAL, NOMINAL, ORDINAL, NOMINAL, ORDINAL, NOMINAL,  NOMINAL, NOMINAL, NOMINAL, NOMINAL, ORDINAL, ORDINAL, ORDINAL]
# ATTRI_TYPE = {
#     'age': ORDINAL,
#     'workclass' : NOMINAL,
#     'fnlwgt' : ORDINAL,
#     'education' : NOMINAL, 
#     'education-num' : ORDINAL,
#     'marital-status' : NOMINAL, 
#     'occupation': NOMINAL,
#     'relationship' : NOMINAL,
#     'race' : NOMINAL,
#     'sex' : NOMINAL,
#     'capital-gain' : ORDINAL,
#     'captial-loss' : ORDINAL,
#     'hours-per-week' : ORDINAL,
# }

# prevent exceeding field limits.
csv.field_size_limit(sys.maxsize)


def read_test_data(testDataPath):
    """Reads test data from .data file.

    Reads the data record line by line and removes the non-data record and the
    record that contains missing data (i.e., ' ?'). Trims labels by eliminating
    the dot sign '.' at the end.

    Parameters
    ----------
    dataFilePath:
        test data set file path related to the project root in string.

    Returns
    -------
    attributes
        a list of lists of attributes without missing data.
    labels
        a list of labels. e.g., 0 for <= 50K, 1 for >50K
    headers
        a list of attributes' names.
    types
        a list of attribute types, i.e., ordinal or nominal.
    """

    attributes = []
    labels = []
    with open(testDataPath, newline='') as datafile:
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
                # if ATTRI_TYPE[HEADERS[i]] == ORDINAL:
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


def read_training_data(dataFilePath):
    """Reads training data from .data file.

    Reads the data record line by line and removes the non-data record and the
    record that contains missing data (i.e., ' ?'). 

    Parameters
    ----------
    dataFilePath:
        test data set file path related to the project root in string.

    Returns
    -------
    attributes
        a list of lists of attributes without missing data.
    labels
        a list of labels. e.g., 0 for <= 50K, 1 for >50K
    headers
        a list of attributes' names.
    types
        a list of attribute types, i.e., ordinal or nominal.
    """
    attributes = []
    labels = []
    with open(dataFilePath, newline='') as datafile:
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
                # if ATTRI_TYPE[HEADERS[i]] == ORDINAL:
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
    