import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import IsolationForest
from sklearn.datasets import make_blobs

# Ler o Banco de dados
data = pd.read_csv("[4] Aprendizado Não-Supervisionado/contracheque.csv")
# Retira os dados que possui algum valor NaN
data = data.dropna()

random_state = np.random.RandomState(42)
# Função do Isolation Forest
model = IsolationForest(
    n_estimators=100,
    max_samples="auto",
    contamination=float(0.1),
    random_state=random_state,
)
X = model.fit(data[["rendimento_liquido"]])
data["anomaly"] = model.predict(data[["rendimento_liquido"]])
data.head(20)

anomaly = data.loc[data["anomaly"] == -1]
anomaly_index = list(anomaly.index)
print(anomaly)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=data.index,
    y=data["rendimento_liquido"],
    hue=data["anomaly"],
    palette={1: "blue", -1: "red"},
)
plt.title("Detecção de Anomalias com Isolation Forest")
plt.show()
