#importing all the libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.metrics import roc_curve, auc

#loading the dataset using Pandas
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
df.head()# Output shown below

# checking whether the dataset contains any missing values...

df.shape == df.dropna().shape # Output shown below


y_bar = np.array([df[df['Attrition']=='No'].shape[0] ,df[df['Attrition']=='Yes'].shape[0]])

x_bar = ['No (0)', 'Yes (1)']
# Bar Visualization
plt.bar(x_bar, y_bar)
plt.xlabel('Labels/Classes')
plt.ylabel('Number of Instances')
plt.title('Distribution of Labels/Classes in the Dataset')

# Label Encoding for Categorical/Non-Numeric Data

X = df.iloc[:,[0] + list(range(2,35))].values

y = df.iloc[:,1].values

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1 = LabelEncoder()
X[:,1] = labelencoder_X_1.fit_transform(X[:,1])
X[:,3] = labelencoder_X_1.fit_transform(X[:,3])
X[:,6] = labelencoder_X_1.fit_transform(X[:,6])
X[:,10] = labelencoder_X_1.fit_transform(X[:,10])
X[:,14] = labelencoder_X_1.fit_transform(X[:,14])
X[:,16] = labelencoder_X_1.fit_transform(X[:,16])
X[:,20] = labelencoder_X_1.fit_transform(X[:,20])
X[:,21] = labelencoder_X_1.fit_transform(X[:,21])
y = labelencoder_X_1.fit_transform(y)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X,y) # Output shown below
list_importances=list(model.feature_importances_)
indices=sorted(range(len(list_importances)), key=lambda k:list_importances[k])
feature_selected=[None]*34
k=0
for i in reversed(indices):
    if k<=33:
        feature_selected[k]=i
    k=k+1
X_selected = X[:,feature_selected[:17]]
l_features=feature_selected
i=0
for x in feature_selected:
    l_features[i] = df.columns[x]
    i=i+1
l_features = np.array(l_features)
# Extracting 17 most important features among 34 features
l_features[:17] #Output shown below

# Selecting the 17 most important features

df_features = pd.DataFrame(X_selected, columns=['Age',
                                                'MonthlyIncome', 'OverTime',
                                                'EmployeeNumber', 'MonthlyRate',
                                                'DistanceFromHome', 'YearsAtCompany',
                                                'TotalWorkingYears', 'DailyRate',
                                                'HourlyRate', 'NumCompaniesWorked',
                                                'JobInvolvement', 'PercentSalaryHike',
                                                'StockOptionLevel','YearsWithCurrManager',
                                                'EnvironmentSatisfaction','EducationField', 'Attrition'])

df_features.head() # Output shown below


# Label Encoding for selected Non-Numeric Features:

X = df_features.iloc[:,list(range(0,17))].values
y = df_features.iloc[:,17].values
X[:,2] = labelencoder_X_1.fit_transform(X[:,2])
X[:,16] = labelencoder_X_1.fit_transform(X[:,16])
y = labelencoder_X_1.fit_transform(y)

# 80-20 splitting where 80% Data is for Training the Model
# and 20% Data is for Validation and Performance Analysis
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=1753)

# Using Logistic Regression Algorithm for Model Training
from sklearn.linear_model import LogisticRegression
clf= LogisticRegression(verbose = 3)
# Training the Model
clf_trained = clf.fit(X_train, y_train) #Output shown below

clf_trained.score(X_train,y_train) # Output shown below
clf_trained.score(X_test,y_test) # Output shown below
# getting the predictions...

predictions=clf_trained.predict(X_test)
print(classification_report(y_test,predictions))


# MODULE FOR CONFUSION MATRIX

import matplotlib.pyplot as plt

import numpy as np

import itertools

def plot_confusion_matrix(cm, classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):

    """
     This function prints and plots the confusion matrix.
     Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:

        print('Confusion matrix, without normalization')
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),horizontalalignment="center",color="white" if cm[i, j] > thresh else "black")
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        # Generating the Confusion Matrix
        plt.figure()

    cm = np.array([[252, 1], [31, 10]])
    plot_confusion_matrix(confusion_matrix(y_test,predictions),classes=[0,1], normalize=True, title='Normalized Confusion Matrix')

    # Output shown below

    # Plotting the ROC Curve

y_roc = np.array(y_test)

fpr, tpr, thresholds = roc_curve(y_roc, clf_trained.decision_function(X_test))

roc_auc = auc(fpr, tpr)

pl.clf()

pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)

pl.plot([0, 1], [0, 1], 'k--')

pl.xlim([0.0, 1.0])

pl.ylim([0.0, 1.0])

pl.xlabel('False Positive Rate')

pl.ylabel('True Positive Rate')

pl.legend(loc="lower right")

pl.show() # Output shown below