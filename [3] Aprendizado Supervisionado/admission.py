"""
treinamento de uma árvore decisão sobre o dataset Admission_Predict
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import pydotplus
import os

# Lendo o dataset escolhido
train_df = pd.read_csv(
    "C:\\Users\\byel3\\OneDrive\\Área de Trabalho\\SISTEMAS INTELIGENTES\\[3] Aprendizado Supervisionado\\Admission_Predict_Ver1.1.csv"
)

# Trocamos a % de chance de ser aceito por valores 0 e 1, 50% ou mais vira 1, <50% é 0

train_df["chanceOfAdmit"] = train_df["chanceOfAdmit"].apply(
    lambda chanceOfAdmit: 0 if chanceOfAdmit < 0.5 else 1
)

# Objetivo é saber se é admitido ou não
classes = ["No", "Yes"]  # 0 or 1
labels = "chanceOfAdmit"
y = train_df["chanceOfAdmit"].values

columns = [
    "GREScore",
    "TOEFLScore",
    "UniversityRating",
    "SOP",
    "LOR",
    "CGPA",
    "Research",
]
features = train_df[list(columns)].values

imp = SimpleImputer(missing_values=np.nan, strategy="mean")
X = imp.fit_transform(features)

clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(X, y)

os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz\\bin"

for i in range(10):
    tree_teste = clf.estimators_[i]
    dot_data_teste = tree.export_graphviz(
        tree_teste,
        feature_names=columns,
        filled=True,
        max_depth=2,
        impurity=False,
        proportion=True,
    )
    graph_teste = pydotplus.graph_from_dot_data(dot_data_teste)
    graph_teste.write_png(f"tree_random{i}.png")

GREScore = 340
TOEFLScore = 120
UniversityRating = 1
SOP = 5
LOR = 5
CGPA = 10
Research = 1

print(clf.predict([[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA, Research]]))
# Predict probability of decision per class

print(
    clf.predict_proba(
        [[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA, Research]]
    )
)
Y_pred = clf.predict(X)
score = accuracy_score(y, Y_pred)

print(score)
