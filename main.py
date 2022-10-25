import sys
import preproc
from DecisionTree import DecisionTree

# #generate a training dataset from the lecture
# def generate_debug_training_set():
#     X_train = [[28, 'high school', 'self-employed'],
#                [32, 'master', 'programmer'],
#                [33, 'undergrad', 'lawyer'],
#                [37, 'undergrad', 'programmer'],
#                [40, 'undergrad', 'self-employed'],
#                [45, 'master', 'self-employed'],
#                [48, 'high school', 'programmer'],
#                [50, 'master', 'lawyer'],
#                [52, 'master', 'programmer'],
#                [55, 'high school', 'self-employed']
#                ]
#     y_train =  [1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
#     headers = ['age', 'education', 'occupation']
#     types = {'age': 'ordinal',
#              'education': 'nominal',
#              'occupation': 'nominal'}
#     return X_train, y_train, headers, types


if __name__ == '__main__':
    num_args = len(sys.argv)
    cut_threshold = 0
    out_path = ''
    cut_flag = False
    out_flag = False
    path_train = './rawData/adult.data'
    path_test = './rawData/adult.test'
    if(num_args > 1):
        for i in range(1, num_args):
            if(sys.argv[i] == '-c'):
                try:
                    cut_threshold = int(sys.argv[i+1])
                    cut_flag = True
                except:
                    print('[ERROR] Missing or Wrong Parameters! The cut_threshold should be an integer >= 1')
                    exit(1)
            elif(sys.argv[i] == '-o'):
                try:
                    out_path = sys.argv[i+1]
                    out_flag = True
                except:
                    print('[ERROR] Missing or Wrong Parameters!')
                    exit(1)
        if(sys.argv[1] != '-c' and sys.argv[1] != '-o'):
            try:
                path_train = sys.argv[1]
                path_test = sys.argv[2]
            except:
                print('[ERROR] Invalid input data path! Please check the usage: ')
                print('\t python main.py <data_path_train> <data_path_test> [options ...]')
                exit(1)
        
    X_train, y_train, headers, attr_types = preproc.read_training_data(path_train)
    if(not cut_flag):
        cut_threshold = int(0.0022 * len(X_train))
    # X_train, y_train, headers, attr_types = generate_debug_training_set()
    decision_tree = DecisionTree(headers, attr_types)
    
    print('Input data path: ')
    print('\t' + path_train)
    print('\t' + path_test)
    print('Cut threshold = ' + str(cut_threshold))
    print()
    print('=====================================')
    decision_tree.fit(X_train, y_train, cut_threshold)
    
    
    if(not out_flag):
        out_path = 'output.txt'

    decision_tree.dfs_print(out_path)
      
    X_test, y_test, _, _= preproc.read_test_data(path_test)
    y_pred = decision_tree.predict(X_test)
    emp_err = decision_tree.empirical_err(y_pred, y_test)
    #Exporting the final report for evaluation set to see whether they are classified successfully.
    classifier = list(map(lambda x, y: 1 if x != y else 0, y_pred, y_test))
    samples_test = X_test
    for i in range(len(y_test)):
        if(y_test[i]==1):
            samples_test[i].append('>50K')
        else:
            samples_test[i].append('<=50K')

    with open("predicted_result.txt", mode="w") as file:
        file.write('Empirical Error = ' + str(emp_err))
        file.write('\n------------------------------------------------------------------------------------------------\n')
        for i in range(len(samples_test)):
            if(classifier[i]==0):
                file.write(str(samples_test[i]))
                file.write('  Correct Predicted!\n')
            else:
                file.write(str(samples_test[i]))
                file.write('  Wrong Predicted!\n')



    
    
