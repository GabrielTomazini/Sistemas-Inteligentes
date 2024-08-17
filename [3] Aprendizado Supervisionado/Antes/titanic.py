# -*- coding: utf-8 -*-
"""
Exemplo de treinamento de uma árvore decisão sobre o dataset Titanic

Lembre-se de configurar o caminho do graphviz (linha 47)

@author: Prof. Daniel Cavalcanti Jeronymo
Atualizado em 08/2020 - a biblioteca sklearn mudou a sintaxe do Imputer
"""


import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn import tree
import pydotplus
import os

# Read dataset into data frame
train_df = pd.read_csv(
    "C:\\Users\\byel3\\OneDrive\\Área de Trabalho\\SISTEMAS INTELIGENTES\\[3] Aprendizado Supervisionado\\Antes\\titanic-train.csv"
)
# Change textual labels 'male' to 0 and 'female' to 1
train_df["Sex"] = train_df["Sex"].apply(lambda sex: 0 if sex == "male" else 1)
# or
# df.Sex[df["Sex"]=='female'] = 1
# df.Sex[df["Sex"]=='male'] = 0

# Define labels (output) as Survived
# Survived is the target, that we want to predict from the values of the other columns
classes = ["No", "Yes"]  # 0 or 1
labels = "Survived"
y = train_df["Survived"].values

# Not all of the other columns are helpful for classification
# So we choose a feature set by hand and convert the features into a numpy array for scikit learn
columns = ["Fare", "Pclass", "Sex", "Age", "SibSp"]
features = train_df[list(columns)].values

# Replace 'nans' by mean to avoid issues
imp = SimpleImputer(missing_values=np.nan, strategy="mean")
print(imp)
X = imp.fit_transform(features)

# Learn the decision tree
clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf = clf.fit(X, y)

os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz\\bin"

# Export as png or pdf
# dot_data = tree.export_graphviz(clf, out_file=None, feature_names=columns)
dot_data = tree.export_graphviz(
    clf,
    out_file=None,
    feature_names=columns,
    class_names=classes,
    filled=True,
    rounded=True,
    special_characters=True,
)
graph = pydotplus.graph_from_dot_data(dot_data)
# graph.write_pdf("titanic.pdf")
graph.write_png("titanic.png")


# Predict using our model
age = 5
pclass = 2
sex = 0
fare = 13
sibsp = 1

# Predict a single decision, survive or not?
print(clf.predict([[fare, pclass, sex, age, sibsp]]))

# Predict probability of decision per class
print(clf.predict_proba([[fare, pclass, sex, age, sibsp]]))
