import streamlit as st
import pandas as pd
import requests
from io import StringIO
import plotly.express as px

def load_pede_data():
    github_csv_url = 'https://raw.githubusercontent.com/aamandanunes/datathon/main/Dataset/PEDE_PASSOS_DATASET_FIAP.csv'
    response = requests.get(github_csv_url)

    csv_content = response.content.decode('utf-8')
    csv_string_io = StringIO(csv_content)
    
    return pd.read_csv(csv_string_io, sep=';')

def analise_pede():
    df = load_pede_data()
    
    df['2020'] = df['FASE_TURMA_2020'].apply(lambda x: 1 if pd.notna(x) else 0)
    df['2021'] = df['TURMA_2021'].apply(lambda x: 1 if pd.notna(x) else 0)
    df['2022'] = df['TURMA_2022'].apply(lambda x: 1 if pd.notna(x) else 0)

    alunos_por_ano = df[['2020', '2021', '2022']].sum().reset_index()
    alunos_por_ano.columns = ['index', 'values']
    fig = px.bar(alunos_por_ano, x="index", y="values", title='Quantidade de Alunos por Ano', labels=dict(values="Quantidade de Alunos", index="Ano"))
    fig.update_xaxes(tickvals=alunos_por_ano['index'])
    fig.update_layout(title_text = 'Quantidade de Alunos por Ano', title_x = 0.35)

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    #Calcular a porcentagem de alunos que atingiram o ponto de virada em cada ano
    df['PONTO_VIRADA_2020'] = df['PONTO_VIRADA_2020'].map({'Sim': True, 'Não': False})
    df['PONTO_VIRADA_2021'] = df['PONTO_VIRADA_2021'].map({'Sim': True, 'Não': False})
    df['PONTO_VIRADA_2022'] = df['PONTO_VIRADA_2022'].map({'Sim': True, 'Não': False})
    
    porcentagem_ponto_virada_2020 = df['PONTO_VIRADA_2020'].mean() * 100
    porcentagem_ponto_virada_2021 = df['PONTO_VIRADA_2021'].mean() * 100
    porcentagem_ponto_virada_2022 = df['PONTO_VIRADA_2022'].mean() * 100

    data = {
        'Ano': ['2020', '2021', '2022'],
        'Ponto_Virada': [porcentagem_ponto_virada_2020, 
                                                    porcentagem_ponto_virada_2021, 
                                                    porcentagem_ponto_virada_2022]
    }
    df_porcentagem = pd.DataFrame(data)   

    # Preencher valores NaN com zero
    df_porcentagem['Ponto_Virada'].fillna(0, inplace=True)

    fig = px.pie(values=df_porcentagem['Ponto_Virada'], names=df_porcentagem['Ano'], title = 'Alunos que atingiram o Ponto de Virada por Ano')
    fig.update_layout(title_text = 'Alunos que atingiram o Ponto de Virada por Ano', title_x = 0.2)
    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)
