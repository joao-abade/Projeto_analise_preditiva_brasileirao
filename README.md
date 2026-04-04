Análise Preditiva do Brasileirão2024 
Modelo de Machine Learning para previsão de resultados de partidas do Campeonato Brasileiro Série A 2024.

Sobre o Projeto
Este projeto utiliza inteligência artificial para prever os resultados dos jogos do Campeonato Brasileiro. O objetivo foi construir um pipeline completo de dados, desde a extração e tratamento até o treinamento de um modelo de Machine Learning capaz de superar a aleatoriedade estatística do esporte.

Tecnologias Utilizadas
Linguagem: Python 3.13
Manipulação de Dados: Pandas e NumPy
Banco de Dados: SQLite (Data Lake local)
Machine Learning: Scikit-Learn (Algoritmo Random Forest)
Versionamento: Git/GitHub

Modelagem e Resultados
Foi utilizado o algoritmo Random Forest Classifier. Após rodadas de ajustes de hiperparâmetros e um forte trabalho de Feature Engineering (incluindo o saldo técnico das equipes), o modelo atingiu:
Precisão Final: 48%
Performance: ~15% superior ao baseline aleatório.
Este resultado é bastante expressivo para uma primeira versão de modelo, considerando que modelos profissionais de casas de apostas operam em faixas próximas a 53-58% de acerto.

Estrutura do Projeto
A arquitetura foi dividida seguindo as melhores práticas de pipelines de dados:

Plaintext
 Projeto_analise_preditiva_brasileirao
 ┣ data/                   # Armazenamento local
 ┃ ┣ brasileirao_predict.db  # Dados brutos
 ┃ ┗ tb_modelagem.db         # Features prontas para IA
 ┣ src/                    # Código-fonte
 ┃ ┣ data_prep/            # Extração e Ingestão (ETL)
 ┃ ┃ ┣ setup_db.py           
 ┃ ┃ ┣ ingest_api_football.py
 ┃ ┃ ┣ weather_api.py        
 ┃ ┃ ┗ ingest_clima.py       
 ┃ ┣ engineering/          # Transformação e Feature Engineering
 ┃ ┃ ┣ enrich_weather.py     
 ┃ ┃ ┗ feature_engineering.py
 ┃ ┗ modeling/             # Inteligência Artificial
 ┃   ┗ model_training.py     
 ┣ requirements.txt        # Dependências do projeto
 ┗ README.md               # Documentação principal
Como Executar
Instale as dependências: pip install -r requirements.txt

Execute a extração: python src/data_prep/setup_db.py

Gere as variáveis analíticas: python src/engineering/feature_engineering.py

Treine o modelo: python src/modeling/model_training.py

Próximos Passos (Backlog)
Expandir o banco de dados para incluir o histórico dos últimos 5 anos do campeonato.

Implementar validação cruzada cronológica (Time Series Split) para evitar embaralhamento do tempo.

Testar algoritmos de boosting (como XGBoost ou Regressão Logística).
