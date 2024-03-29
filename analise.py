import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from io import BytesIO
import plotly.express as px

def realizar_analise():

    github_csv_url = 'https://raw.githubusercontent.com/aamandanunes/datathon/main/Dataset/PEDE_PASSOS_DATASET_FIAP.csv'
    response = requests.get(github_csv_url)

    csv_content = response.content.decode('utf-8')
    csv_string_io = StringIO(csv_content)
    df = pd.read_csv(csv_string_io, sep=';')

    github_xlsx_url = 'https://raw.githubusercontent.com/aamandanunes/datathon/main/Dataset/PSE2020_domicilios.xlsx'
    response = requests.get(github_xlsx_url)

    xlsx_content = response.content
    xlsx_bytes_io = BytesIO(xlsx_content)
    df2 = pd.read_excel(xlsx_bytes_io)
    df2.columns=['Código do domicilio','Ano de referência','Total de moradores','Código do entrevistador','Código do Núcleo PM','Condição no domicílio','Cônjuge de sexo diferente','Cônjuge do mesmo sexo','Total de filhos ou enteados','Cônjuge no domicílio','Filhos ou enteados no domicílio','Arranjo familiar','Sexo do responsável','Total de homens no domicíio','Total de mulheres no domicílio','Idade do responsável','Cor ou Raça do responsável','Relação do responsável com a APM','Total de alunos Passos Mágicos','Total de bolsistas','Total bolsistas Decisão','Total bolsistas João Paulo II','Total bolsistas Einstein','Total bosistas FIAP','Total bolsistas UNISA','Total bolsistas Estácio','Total bolsistas Outros','Total de inativos Passos Mágicos','Total PIT','Total PO','Total PD','Total trabalhadores infantis','Total FFT','Total FT','Total desempregados de longo prazo','Total trabalhadores formais','Total trabalhadores informais','Privação trabalho formal','Valor total rendas do trabalho','Total indivíduos BPC/LOAS','Valor total BPC/LOAS','Total indivíduos Bolsa Família','Valor total Bolsa Família','Total indivíduos Outros Programas','Valor total Outros Programas','Total indivíduos Aposentadoria','Valor total Aposentadoria','Total indivíduos Seguro desemprego','Valor total Seguro desemprego','Total indivíduos Pensão ou mesada','Valor total Pensão ou mesada','Total indivíduos Aluguel','Valor total Aluguel','Valor total Rendas Programas Sociais','Valor total Outras Rendas','Valor Renda total do domicílio','Origem da renda','Renda per capita','Renda per capita em faixas','Renda total em faixas','Linhas pobreza','Tipo do domicílio','Material predominante do piso','Quantos cômodos?','Quantos dormitórios?','Disponibilidade de água encanada','Quantos banheiros exclusivos?','Quantos banheiros compartilhados?','Forma de escoamento do esgoto?','Origem da energia elétrica?','Combustível usado para cozinhar?','Caracterize a propriedade do domicílio','Quantos moradores possuem telefone celular?','Possui telefone fixo?','Tem geladeira ou freezer?','Tem televisor?','Tem computador?','Tem acesso à internet?','Tem internet via celular?','Tem automóvel?','#N/D']
    df2.drop('#N/D', inplace=True, axis=1)
    df2['Ano de referência'] = pd.to_datetime(df2['Ano de referência'], format='%Y')

    aba1, aba2 = st.tabs(['Análise', 'Dados Brutos'])    
    with aba2:
        st.write("PEDE")
        st.write(df.head())
        st.write("PSE")
        st.write(df2.head())       
    with aba1:
        #Criar novas colunas para marcar se foi aluno ou naquele ano
        df['2020'] = df['FASE_TURMA_2020'].apply(lambda x: 1 if pd.notna(x) else 0)
        df['2021'] = df['TURMA_2021'].apply(lambda x: 1 if pd.notna(x) else 0)
        df['2022'] = df['TURMA_2022'].apply(lambda x: 1 if pd.notna(x) else 0)
    
        alunos_por_ano = df[['2020', '2021', '2022']].sum().reset_index()
        alunos_por_ano.columns = ['index', 'values']
        fig = px.bar(alunos_por_ano, x="index", y="values", title='Quantidade de Alunos por Ano', labels=dict(values="Ano", index="Quantidade de Alunos"))
        
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

        fig, ax = plt.subplots()
        ax.pie(df_porcentagem['Ponto_Virada'], labels=df_porcentagem['Ano'], autopct='%1.1f%%')
        ax.set_title('Alunos que atingiram o Ponto de Virada por Ano')
        st.pyplot(fig)

        #Alunos bairro
        alunos_por_bairro = df2['Código do Núcleo PM'].value_counts().reset_index()
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
