import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from geopy.geocoders import Nominatim

def realizar_analise():

    aba1, aba2 = st.tabs(['Análise', 'Dados Brutos'])    
    with aba2:
        st.write("PEDE")
        df = pd.read_csv("Dataset/PEDE_PASSOS_DATASET_FIAP.csv", sep=';')
        st.write(df.head())
        st.write("PSE")
        df2 = pd.read_excel("Dataset/PSE2020_domicilios.xlsx")
        st.write(df2.head())       
    with aba1:
        #Criar novas colunas para marcar se foi aluno ou naquele ano
        df['2020'] = df['FASE_TURMA_2020'].apply(lambda x: 1 if pd.notna(x) else 0)
        df['2021'] = df['TURMA_2021'].apply(lambda x: 1 if pd.notna(x) else 0)
        df['2022'] = df['TURMA_2022'].apply(lambda x: 1 if pd.notna(x) else 0)
    
        alunos_por_ano = df[['2020', '2021', '2022']].sum()

        fig, ax = plt.subplots()
        ax.bar(alunos_por_ano.index, alunos_por_ano.values)
        ax.set_xlabel('Ano')
        ax.set_ylabel('Quantidade de Alunos')
        ax.set_title('Quantidade de Alunos por Ano')
        st.pyplot(fig)
        
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

        fig, ax = plt.subplots()
        ax.pie(df_porcentagem['Ponto_Virada'], labels=df_porcentagem['Ano'], autopct='%1.1f%%')
        ax.set_title('Alunos que atingiram o Ponto de Virada por Ano')
        st.pyplot(fig)

        #Alunos bairro
        alunos_por_bairro = df2['V102_first'].value_counts().reset_index()
        alunos_por_bairro.columns = ['Bairro', 'Total de Alunos']
        alunos_por_bairro = alunos_por_bairro.sort_values(by='Total de Alunos', ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(alunos_por_bairro['Bairro'], alunos_por_bairro['Total de Alunos'], color='skyblue')

        ax.set_xlabel('Total de Alunos')
        ax.set_ylabel('Bairro')
        ax.set_title('Total de Alunos por Bairro')

        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, '{:,}'.format(int(width)), va='center', ha='left')
        st.pyplot(fig)
