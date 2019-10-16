# importing all the libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

os.chdir("D:/work_files/pycharm_codes/nlp_assignment")


def read_hr_data():
    return pd.read_csv('homework/logistic_model/data/WA_Fn-UseC_-HR-Employee-Attrition.csv')


def plot_attrition():
    """
    绘制是否流失的数据情况
    :return: void
    """
    df = read_hr_data()
    y_bar = np.array([df[df['Attrition'] == 'No'].shape[0], df[df['Attrition'] == 'Yes'].shape[0]])
    x_bar = ['No (0)', 'Yes (1)']
    # Bar Visualization
    plt.bar(x_bar, y_bar)
    plt.xlabel('Labels/Classes')
    plt.ylabel('Number of Instances')
    plt.title('Distribution of Labels/Classes in the Dataset')
    plt.show()


def test_random_forest_classifier():
    """
    根据数据进行随机森林分类器训练
    :return: void
    """
    X = df.iloc[:, [0] + list(range(2, 35))].values  # 除了第2列的所有值
    y = df.iloc[:, 1].values
    labelencoder_X_1 = LabelEncoder()
    # 对每个标签指标进行数值化转化
    X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])  # BusinessTravel 出差频次
    X[:, 3] = labelencoder_X_1.fit_transform(X[:, 3])  # Department 部门
    X[:, 6] = labelencoder_X_1.fit_transform(X[:, 6])  # EducationField 教育类型
    X[:, 10] = labelencoder_X_1.fit_transform(X[:, 10])  # Gender 性别
    X[:, 14] = labelencoder_X_1.fit_transform(X[:, 14])  # JobRole 职务
    X[:, 16] = labelencoder_X_1.fit_transform(X[:, 16])  # MaritalStatus 婚姻状况
    X[:, 20] = labelencoder_X_1.fit_transform(X[:, 20])  # Over18 是否过18岁
    X[:, 21] = labelencoder_X_1.fit_transform(X[:, 21])  # OverTime 是否加班
    y = labelencoder_X_1.fit_transform(y)
    # Feature Selection using Random Forest Classifier's Feature
    # Importance Scores
    model = RandomForestClassifier()
    model.fit(X, y)  # Output shown below
    list_importances = list(model.feature_importances_)
    indices = sorted(range(len(list_importances)), key=lambda k: list_importances[k])
    feature_selected = [None] * 34
    k = 0
    for i in reversed(indices):
        if k <= 33:
            feature_selected[k] = i
        k = k + 1
    X_selected = X[:, feature_selected[:17]]  # 选择对应特征的数据集
    l_features = feature_selected
    i = 0
    for x in feature_selected:  # 选择对应特征的特征名称
        if x >= 1:
            l_features[i] = df.columns[x + 1]  # 这边因为抽数的原因>=1的索引非原始数据列索引
        else:
            l_features[i] = df.columns[x]
        i = i + 1
    l_features = np.array(l_features)  # 根据选出来的17个特征产生特征df,最后一个特征为流失特征
    df_features = pd.DataFrame(X_selected, columns=['Age', 'MonthlyIncome', 'MonthlyRate', 'DailyRate', 'OverTime',
                                                    'DistanceFromHome', 'EmployeeNumber', 'HourlyRate',
                                                    'TotalWorkingYears', 'YearsAtCompany', 'NumCompaniesWorked',
                                                    'YearsInCurrentRole', 'PercentSalaryHike',
                                                    'RelationshipSatisfaction', 'YearsWithCurrManager',
                                                    'EducationField', 'JobInvolvement', 'Education', 'JobRole',
                                                    'StockOptionLevel', 'YearsSinceLastPromotion',
                                                    'EnvironmentSatisfaction', 'JobSatisfaction',
                                                    'TrainingTimesLastYear', 'MaritalStatus', 'WorkLifeBalance',
                                                    'JobLevel', 'BusinessTravel', 'Department', 'Gender',
                                                    'PerformanceRating', 'StandardHours', 'Over18', 'EmployeeCount',
                                                    "Attrition"])



if __name__ == '__main__':
    df = read_hr_data()
    test_random_forest_classifier()
