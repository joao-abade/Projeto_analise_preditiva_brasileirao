import pandas as pd
import sqlite3

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('tb_modelagem.db')

df_model = pd.read_sql('SELECT * FROM model_input', conn)

conn.close()

df_ml = df_model.copy()
print(f"Total de linhas no dataset: {len(df_ml)}")

df_ml = pd.get_dummies(df_ml, columns=['mandante', 'visitante'], dtype=int)

y = df_ml['resultado']
x = df_ml.drop(columns=['resultado', 'data'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=20)

forest_model = RandomForestClassifier(n_estimators=100, random_state=20)

forest_model.fit(x_train, y_train)

previsoes = forest_model.predict(x_test)

precisao = accuracy_score(y_test, previsoes)

print(previsoes)
print(precisao)