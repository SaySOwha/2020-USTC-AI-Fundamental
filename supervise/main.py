import pandas as pd 
import numpy as np
from sklearn import preprocessing
from KNN import *
from SVM import *


def calc_F1_score(predict_label, truth_label):
    '''
        Function: calculate F1 score 
        Param: predict_label, truth_label
        Return: list: [F1, Precision, Recall] 
    '''
    compare = predict_label - truth_label 
    FP = len(compare[compare == 2]) # predict = 1, truth = -1
    FN = len(compare[compare == -2]) # predict = -1, truth = 1
    
    compare = predict_label + truth_label
    TP = len(compare[compare == 2]) # predict = 1, truth = 1
    TN = len(compare[compare == -2]) # predict = -1, truth = -1

    print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")

    try:
        P = TP / (TP + FP) # precision
        R = TP / (TP + FN) # recall
        F1 = 2 * P * R / (P + R)
        print(f"F1 score: {F1}, Precision: {P}, Recall: {R}")
        return [F1, P, R, TP, FP, TN, FN] 
    except ZeroDivisionError:
        print("divide zero!")


def main():
    math_data = pd.read_csv('data/student/student-mat.csv', sep=';')
    # por_data = pd.read_csv('data/student/student-por.csv', sep=';')

    # select feature 
    feature_name = ['G1','G2','G3']
    data = math_data[feature_name]
    # data = math_data

    # G3 == 1: pass, G3 == 0: fail
    data.G3[data.G3 < 10] = -1 # 0 or -1  
    data.G3[data.G3 >= 10] = 1
    # other preprocessing here  #TODO

    # train data and test data partition
    train_data = data.sample(frac = 0.7, axis = 0)
    test_data = data[~data.index.isin(train_data.index)]

    train_label = train_data['G3'].to_numpy()
    test_label = test_data['G3'].to_numpy()

    del train_data['G3']
    del test_data['G3']

    # label encode
    train_data = train_data.apply(preprocessing.LabelEncoder().fit_transform)
    test_data = test_data.apply(preprocessing.LabelEncoder().fit_transform)
    
    # normalize data 
    train_data = train_data / train_data.max(axis = 0)
    test_data = test_data / test_data.max(axis = 0)

    print(train_data)

    train_data = train_data.to_numpy()
    test_data = test_data.to_numpy()

    print(f"train data size: {train_data.shape[0]}, test data size: {test_data.shape[0]}")

    # test_knn(train_data, train_label, test_data, test_label, 9)

    #SVM_fit(train_data, train_label, kernel_linear, 100)

    test_SVM(train_data, train_label, test_data, test_label, "linear", 500)
    
if __name__ == "__main__":
    main()