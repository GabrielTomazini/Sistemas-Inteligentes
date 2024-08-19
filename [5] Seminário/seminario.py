"""
Autores: Gabriel Tomazini Marani 2266083
         Paulo Victor Nogueira Rodrigues 2265125
Treinamento de uma árvore decisão sobre o dataset Admission_Predict
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression

# Lendo o dataset escolhido
train_df = pd.read_csv(
    "C:\\Users\\byel3\\OneDrive\\Área de Trabalho\\SISTEMAS INTELIGENTES\\[3] Aprendizado Supervisionado\\Admission_Predict_Ver1.1.csv"
)
y_reg = train_df["chanceOfAdmit"].values

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

# Aqui, separamos o repositório em dados que serão usados para treino e dados utilizados para teste
imp = SimpleImputer(missing_values=np.nan, strategy="mean")
X = imp.fit_transform(features)
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(x_train, y_train)

GREScore = 340
TOEFLScore = 120
UniversityRating = 5
SOP = 5
LOR = 5
CGPA = 10
Research = 1

print(clf.predict([[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA, Research]]))

print(
    clf.predict_proba(
        [[GREScore, TOEFLScore, UniversityRating, SOP, LOR, CGPA, Research]]
    )
)
Y_pred = clf.predict(x_test)
score = accuracy_score(y_test, Y_pred)

print(score)

# Regressão linear
x_train_reg, x_test_reg, y_train_reg, y_test_reg = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

reg = LinearRegression()
reg.fit(x_train_reg, y_train_reg)

y_pred_reg = reg.predict(x_test_reg)
MAE = mean_absolute_error(y_test_reg, y_pred_reg)
MSE = mean_squared_error(y_test_reg, y_pred_reg)

print("==============REGRESSÃO===============")
print("MAE: ")
print(MAE)
print("MSE: ")
print(MSE)
