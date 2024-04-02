import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from io import BytesIO
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

def load_pede_passos():
    github_csv_url = 'https://raw.githubusercontent.com/aamandanunes/datathon/main/Dataset/PEDE_PASSOS_DATASET_FIAP.csv'
    response = requests.get(github_csv_url)

    csv_content = response.content.decode('utf-8')
    csv_string_io = StringIO(csv_content)

    df = pd.read_csv(csv_string_io, sep=';', decimal=".")

    return df

def modeloBolsista(data_simulacao, nome_aluno, dadosInput):
    df = load_pede_passos()
    df_filtrada = df[df['BOLSISTA_2022'].notna()]
    colunas2022 = ['BOLSISTA_2022', 'IAA_2022', 'IEG_2022', 'IPS_2022', 'IDA_2022', 'NOTA_PORT_2022', 'NOTA_MAT_2022', 'NOTA_ING_2022']
    df_filtrada = df_filtrada[colunas2022]
    df_filtrada['BOLSISTA_2022'] = df_filtrada['BOLSISTA_2022'].replace({"Sim": 1, "Não": 0})
    df_filtrada.fillna(0, inplace=True)
    X = df_filtrada.drop('BOLSISTA_2022', axis=1)
    y = df_filtrada['BOLSISTA_2022']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    modeloBolsistas = LogisticRegression()
    modeloBolsistas.fit(X_train_scaled, y_train)
    previsoes = modeloBolsistas.predict(X_test_scaled)
    acuracia = accuracy_score(y_test, previsoes)
    probalibilidade = modeloBolsistas.predict_proba([dadosInput])
    st.write("Probabilidade: ", round(probalibilidade[0,1]*100,2), '%')
    result = probalibilidade[0,1]
    if(result < 0.7):
        texto  = nome_aluno +  " está próximo, só precisa se esforçar um pouco mais! :muscle:"
        st.subheader(texto)
    else:
        texto  = "Há uma grande chance de conseguir uma bolsa de estudo para o(a) " + nome_aluno + ':heartbeat:'
        st.subheader(texto)

    st.write("Acurácia:", acuracia)

    relatorio_classificacao = classification_report(y_test, previsoes)
    st.write("Relatório de classificação:\n", relatorio_classificacao)



