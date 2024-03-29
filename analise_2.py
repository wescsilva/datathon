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

    st.subheader('Total de filhos ou enteados alunos da Passos Mágicos')

    st.write('No gráfico abaixo podemos ver a relação entre a quantidade total de filhos ou enteados no domícilio em relação ao número de alunos da Passos Mágicos.', )
    st.write('A partir dessa relação, conseguimos dimensionar visualmente pelo tamanho dos círculos a quantidade de cada um dos cenários e evidenciar através das cores, quais destes, todos os filhos ou enteados da casa, são alunos da Passos Mágicos')

    df_total_filhos_vs_total_passos = df2.groupby(['Total de filhos ou enteados', 'Total de alunos Passos Mágicos'])['Código do domicilio'].count().reset_index()
    df_total_filhos_vs_total_passos.rename({'Código do domicilio': 'Quantidade de domicílios'}, inplace=True, axis=1)
    df_total_filhos_vs_total_passos['Todos são alunos da Passos Mágicos'] = df_total_filhos_vs_total_passos['Total de filhos ou enteados'] == df_total_filhos_vs_total_passos['Total de alunos Passos Mágicos']
    df_total_filhos_vs_total_passos['Todos são alunos da Passos Mágicos'] = df_total_filhos_vs_total_passos['Todos são alunos da Passos Mágicos'].replace(True, 'Sim').replace(False, 'Não')
    # st.write(df_total_filhos_vs_total_passos)
    fig = px.scatter(df_total_filhos_vs_total_passos, x="Total de filhos ou enteados", y="Total de alunos Passos Mágicos", size="Quantidade de domicílios",
           color='Todos são alunos da Passos Mágicos', log_x=True, size_max=60, color_discrete_map={
                "Sim": "green",
                "Não": "blue"})
        #    hover_name="country", log_x=True, size_max=60)

    # Total de filhos ou enteados por total de alunos na Passos Mágicos - Por residencia --> Barra
    
    # fig = px.scatter(df2, x="Total de filhos ou enteados", y="Total de alunos Passos Mágicos")
    # fig = px.bar(alunos_por_ano, x="index", y="values", title='Quantidade de Alunos por Ano', labels=dict(values="Ano", index="Quantidade de Alunos"))
    fig.update_layout(title_text = 'Total de filhos ou enteados alunos da Passos Mágicos', title_x = 0.2)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
