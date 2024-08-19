"""
Autores: Gabriel Tomazini Marani 2266083
         Paulo Victor Nogueira Rodrigues 2265125
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

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

GREScore = 90
TOEFLScore = 40
UniversityRating = 5
SOP = 1
LOR = 1
CGPA = 2
Research = 0

print(clf.predict([[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA, Research]]))

print(
    clf.predict_proba(
        [[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA, Research]]
    )
)
Y_pred = clf.predict(X)
score = accuracy_score(y, Y_pred)

print(score)
