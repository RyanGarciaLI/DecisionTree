import os
import preproc

DATA_PATH = os.path.join('rawData', 'adult.data')
TEST_PATH = os.path.join('rawData', 'adult.test')

attributes, labels, headers, types = preproc.read_training_data(DATA_PATH)
print(headers)
print(types)
for i in range(0, len(attributes)):
    print(attributes[i], end='|')
    print(labels[i])