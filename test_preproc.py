import preproc

attributes, labels, headers, types = preproc.read_training_data()
print(headers)
print(types)
for i in range(0, len(attributes)):
    print(attributes[i], end='|')
    print(labels[i])