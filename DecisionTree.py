import itertools

# Evaluate the quality of a split given the counts of yes/no in each subset
def gini_of_split(count_left_y, count_left_n, count_right_y, count_right_n):
    N_left = count_left_y + count_left_n
    N_right = count_right_y + count_right_n
    N = N_left + N_right
    if(N_left == 0):
        p_y_left = 0
    else:
        p_y_left = count_left_y/N_left
    p_n_left = 1 - p_y_left
    if(N_right == 0):
        p_y_right = 0
    else:
        p_y_right = count_right_y/N_right
    p_n_right = 1 - p_y_right
    GINI_left = 1 - (p_y_left*p_y_left + p_n_left*p_n_left)
    GINI_right = 1 - (p_y_right*p_y_right + p_n_right*p_n_right)
    return N_left/N*GINI_left + N_right/N*GINI_right

    


class TreeNode:
    def __init__(self, isLeaf):
        self._isLeaf = isLeaf
    
    @property
    def isLeaf(self):
        return self._isLeaf
    
    
    
class InternalNode(TreeNode):
    def __init__(self, split_attr_idx, predicate, left, right):
        super().__init__(False)
        self._split_attr_idx = split_attr_idx
        self._predicate = predicate
        self._left = left
        self._right = right
        
    @property
    def split_attr_idx(self):
        return self._split_attr_idx
    
    @property
    def predicate(self):
        return self._predicate
    
    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right
    
    def predicate_to_string(self):
        predicate_str = '('
        if(isinstance(self._predicate, tuple)):
            for i in range(len(self._predicate) - 1):
                predicate_str += str(self._predicate[i])
                predicate_str += ', '
            predicate_str += str(self._predicate[len(self._predicate) - 1])
            predicate_str += ')'
            return predicate_str
        else:
            return str(self._predicate)
        
        
        
class LeafNode(TreeNode):
    def __init__(self, label):
        super().__init__(True)
        self._label = label
        
    @property
    def label(self):
        return self._label


class DecisionTree:
    def __init__(self, headers, attr_types):
        self._headers = headers
        self._attr_types = attr_types
        self._N_attrs = len(attr_types)
        self._root = None
    
    @property
    def headers(self):
        return self._headers
        
    @property
    def attr_types(self):
        return self._attr_types
    
    @property
    def N_attrs(self):
        return self._N_attrs
    
    def fit(self, X_train, y_train, cut_threshold):
        print('TRAINING......')
        training_samples = X_train
        for i in range(len(y_train)):
            training_samples[i].append(y_train[i])
        self._root = self._hunt(training_samples, cut_threshold)
        print('TRAINING DONE!')
        print()
        
    def predict(self, X_test):
        return [self._predict_instance(X_test[i]) for i in range(len(X_test))]
    
    def dfs_print(self, out_path = None):
        if(out_path):
            with open(out_path, 'w') as fd:
                self._dfs_to_file(self._root, fd, 0, False, '')
                print('The Decision Tree information (DFS order) has been written into ' + out_path)
        else:
            print('==========DFS PRINT==========')
            self._dfs(self._root)
            print('=============================')
        print()
        
    def empirical_err(self, y_pred, y_test):
        N = len(y_pred)
        num_falses = sum(list(map(lambda x, y: 1 if x!=y else 0, y_pred, y_test)))
        return num_falses/N
    
    def _dfs(self, root):
        if(root.isLeaf):
            message = '(label: '
            message += str(root.label)
            message += ') '
            print(message)
        else:
            message = '['
            message += 'split_attribute = '
            message += self.headers[root.split_attr_idx]
            message += '; predicate = '
            message += str(root.predicate)
            message += '] '
            print(message)
            self._dfs(root.left)
            self._dfs(root.right)
            
    def _dfs_to_file(self, root, fd, level=0, isLeft=False, prefix=''):
        if(root.isLeaf):
            message = ''
            message += '(label: '
            message += str(root.label)
            message += ') \n'
            fd.write(prefix + message)
        else:
            if(isLeft):
                pf = prefix + '|\t'
                message = ''
                message += '['
                message += 'split_attribute = '
                message += self.headers[root.split_attr_idx]
                message += '; predicate = '
                message += root.predicate_to_string()
                message += '] \n'
                fd.write(prefix + message)
                self._dfs_to_file(root.left, fd, level + 1, True, pf)
                self._dfs_to_file(root.right, fd, level + 1, False, pf)
            else:
                pf = prefix + '\t'
                message = ''
                message += '['
                message += 'split_attribute = '
                message += self.headers[root.split_attr_idx]
                message += '; predicate = '
                message += root.predicate_to_string()
                message += '] \n'
                fd.write(prefix + message)
                self._dfs_to_file(root.left, fd, level + 1, True, pf)
                self._dfs_to_file(root.right, fd, level + 1, False, pf)


        
    def _predict_instance(self, instance):
        node = self._root
        while(not node.isLeaf):
            if(self.attr_types[node.split_attr_idx]=='ordinal'):
                if(instance[node.split_attr_idx] <= node.predicate):
                    node = node.left
                else:
                    node = node.right
            else:
                if(instance[node.split_attr_idx] in node.predicate):
                    node = node.left
                else:
                    node = node.right
        return node.label
    
    def _hunt(self, training_samples, cut_threshold):
        N_samples = len(training_samples)
        num_y = sum([training_samples[i][-1] for i in range(N_samples)])
        num_n = N_samples-num_y
        
        # If all the objects in S belong to the same class,
        # return a leaf node with the value of this class
        if(num_y == N_samples):
            return LeafNode(1)
        if(num_n == N_samples):
            return LeafNode(0)
        
        # If the sample size is too small, 
        # return a leaf node whose class value is the majority one in S
        if(N_samples <= cut_threshold):
            return LeafNode(1) if num_y>=num_n else LeafNode(0)
        
        # If all the objects in S have the same attribute values
        all_the_same = True
        for i in range(1, N_samples):
            if(not all_the_same):
                break
            for j in range(self.N_attrs):
                if(training_samples[i][j] != training_samples[i-1][j]):
                    all_the_same = False
                    break
        if(all_the_same):
            return LeafNode(1) if num_y>=num_n else LeafNode(0)
        
        # find the "best" split attribute and predicate
        min_GINI = 1
        idx_split_attr = -1
        split_predicate = None
        for i in range(self.N_attrs):
            tmp_predicate = None
            tmp_GINI = 1
            if(self.attr_types[i]=='ordinal'):
                tmp_predicate, tmp_GINI = self._split_ordinal_attr(training_samples, i, num_y, num_n)
            else:
                tmp_predicate, tmp_GINI = self._split_nominal_attr(training_samples, i, num_y, num_n)
            if(tmp_GINI < min_GINI):
                idx_split_attr = i
                min_GINI = tmp_GINI
                split_predicate = tmp_predicate
                
        # split the sample set and create a root with left child and right child
        if(self.attr_types[idx_split_attr]=='ordinal'):
            training_samples.sort(key = lambda x : x[idx_split_attr])
            left_node = self._hunt(training_samples[:split_predicate+1], cut_threshold)
            right_node = self._hunt(training_samples[split_predicate+1:], cut_threshold)
            return InternalNode(idx_split_attr, training_samples[split_predicate][idx_split_attr], left_node, right_node)
        else:
            left_samples = []
            right_samples = []
            for i in range(len(training_samples)):
                if(training_samples[i][idx_split_attr] in split_predicate):
                    left_samples.append(training_samples[i])
                else:
                    right_samples.append(training_samples[i])
            left_node = self._hunt(left_samples, cut_threshold)
            right_node = self._hunt(right_samples, cut_threshold)
            return InternalNode(idx_split_attr, split_predicate, left_node, right_node)
        
    # This function referred to the algorithm in problem 3 of exercise 1 
    def _split_ordinal_attr(self, training_samples, attr_idx, num_y, num_n):
        training_samples.sort(key = lambda x : x[attr_idx])
        split_idx = -1
        min_GINI = 1
        count_left_y = 0
        count_left_n = 0
        count_right_y = num_y
        count_right_n = num_n
        for i in range(len(training_samples)-1):
            if(training_samples[i][-1] == 1):
                count_left_y += 1
                count_right_y -= 1
            else:
                count_left_n += 1
                count_right_n -= 1
            if(training_samples[i][attr_idx]==training_samples[i+1][attr_idx]):
                continue
            else:
                cur_GINI = gini_of_split(count_left_y, count_left_n, count_right_y, count_right_n)
                if(cur_GINI < min_GINI):
                    min_GINI = cur_GINI
                    split_idx = i
        return split_idx, min_GINI
        
            
    def _split_nominal_attr(self, training_samples, attr_idx, num_y, num_n):
        dict_y = {}
        dict_n = {}
        for i in range(len(training_samples)):
            attr_val = training_samples[i][attr_idx]
            if(training_samples[i][-1]==1):
                dict_y[attr_val] = dict_y.get(attr_val, 0) + 1
            else:
                dict_n[attr_val] = dict_n.get(attr_val, 0) + 1
        domain_set = set(dict_y.keys()).union(set(dict_n.keys()))
            
        split_set = set()
        min_GINI = 1
        for i in range(1, len(domain_set)//2 + 1):
            for subset in itertools.combinations(domain_set, i):
                count_left_y = 0
                count_left_n = 0
                for item in subset:
                    count_left_y += dict_y.get(item, 0)
                    count_left_n += dict_n.get(item, 0)
                count_right_y = num_y - count_left_y
                count_right_n = num_n - count_left_n
                cur_GINI = gini_of_split(count_left_y, count_left_n, count_right_y, count_right_n)
                if(cur_GINI < min_GINI):
                    min_GINI = cur_GINI
                    split_set = subset
        return split_set, min_GINI
        
        
        