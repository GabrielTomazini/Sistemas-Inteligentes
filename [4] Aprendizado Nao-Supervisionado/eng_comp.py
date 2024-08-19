"""
Autores: Gabriel Tomazini Marani 2266083
         Paulo Victor Nogueira Rodrigues 2265125
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import sklearn.cluster
import os


def main():
    data = pd.read_csv(
        "C:\\Users\\byel3\\OneDrive\\Área de Trabalho\\SISTEMAS INTELIGENTES\\[4] Aprendizado Nao-Supervisionado\\alunos_engcomp-2023.csv"
    )

    data["Sexo"] = data["Sexo"].apply(lambda Sexo: 0 if Sexo == "F" else 1)

    data["Escola"] = data["Escola"].apply(
        lambda Escola: 0 if Escola == "Particular" else 1
    )
    """
    data["Coeficiente"] = data["Coeficiente"].apply(
        lambda Coeficiente: Coeficiente * 1000
    )"""

    importantData = data[["Sexo", "Coeficiente", "Escola", "Enem"]]
    x = importantData[["Enem", "Escola"]]

    # OBS: minsamples >= D + 1
    db = sklearn.cluster.DBSCAN(eps=10, min_samples=5).fit(x)
    print("Labels", db.labels_)
    print("Unique Labels", np.unique(db.labels_))

    # OBS: This score can be used to determine optimum eps for dbscan, similar to elbow method for kmeans
    db_labels = db.fit_predict(x)
    print("Silhoute score", sklearn.metrics.silhouette_score(x, db_labels))

    for label in np.unique(db.labels_):
        print("LABEL ", label)
        print(importantData.iloc[db.labels_ == label])

    x.plot.scatter(
        x="Escola",
        y="Enem",
        c=db.labels_,
        cmap="Set1",
        edgecolor=(0, 0, 0),
    )
    plt.show()


if __name__ == "__main__":
    # Set the working directory (where we expect to find files) to the same
    # directory this .py file is in. You can leave this out of your own
    # code, but it is needed to easily run the examples using "python -m"
    # as mentioned at the top of this program.
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

    main()
