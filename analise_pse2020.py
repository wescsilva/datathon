import streamlit as st
import pandas as pd
import requests
from io import StringIO
from io import BytesIO
import plotly.express as px

def load_pse2020():
    github_csv_url = 'https://raw.githubusercontent.com/aamandanunes/datathon/main/Dataset/PEDE_PASSOS_DATASET_FIAP.csv'
    response = requests.get(github_csv_url)

    csv_content = response.content.decode('utf-8')
    csv_string_io = StringIO(csv_content)
    df = pd.read_csv(csv_string_io, sep=';')

    github_xlsx_url = 'https://raw.githubusercontent.com/aamandanunes/datathon/main/Dataset/PSE2020_domicilios.xlsx'
    response = requests.get(github_xlsx_url)

    xlsx_content = response.content
    xlsx_bytes_io = BytesIO(xlsx_content)
    df = pd.read_excel(xlsx_bytes_io)
    df.columns=['Código do domicilio','Ano de referência','Total de moradores','Código do entrevistador','Código do Núcleo PM','Condição no domicílio','Cônjuge de sexo diferente','Cônjuge do mesmo sexo','Total de filhos ou enteados','Cônjuge no domicílio','Filhos ou enteados no domicílio','Arranjo familiar','Sexo do responsável','Total de homens no domicíio','Total de mulheres no domicílio','Idade do responsável','Cor ou Raça do responsável','Relação do responsável com a APM','Total de alunos Passos Mágicos','Total de bolsistas','Total bolsistas Decisão','Total bolsistas João Paulo II','Total bolsistas Einstein','Total bosistas FIAP','Total bolsistas UNISA','Total bolsistas Estácio','Total bolsistas Outros','Total de inativos Passos Mágicos','Total PIT','Total PO','Total PD','Total trabalhadores infantis','Total FFT','Total FT','Total desempregados de longo prazo','Total trabalhadores formais','Total trabalhadores informais','Privação trabalho formal','Valor total rendas do trabalho','Total indivíduos BPC/LOAS','Valor total BPC/LOAS','Total indivíduos Bolsa Família','Valor total Bolsa Família','Total indivíduos Outros Programas','Valor total Outros Programas','Total indivíduos Aposentadoria','Valor total Aposentadoria','Total indivíduos Seguro desemprego','Valor total Seguro desemprego','Total indivíduos Pensão ou mesada','Valor total Pensão ou mesada','Total indivíduos Aluguel','Valor total Aluguel','Valor total Rendas Programas Sociais','Valor total Outras Rendas','Valor Renda total do domicílio','Origem da renda','Renda per capita','Renda per capita em faixas','Renda total em faixas','Linhas pobreza','Tipo do domicílio','Material predominante do piso','Quantos cômodos?','Quantos dormitórios?','Disponibilidade de água encanada','Quantos banheiros exclusivos?','Quantos banheiros compartilhados?','Forma de escoamento do esgoto?','Origem da energia elétrica?','Combustível usado para cozinhar?','Caracterize a propriedade do domicílio','Quantos moradores possuem telefone celular?','Possui telefone fixo?','Tem geladeira ou freezer?','Tem televisor?','Tem computador?','Tem acesso à internet?','Tem internet via celular?','Tem automóvel?','#N/D']
    df.drop('#N/D', inplace=True, axis=1)
    df['Ano de referência'] = pd.to_datetime(df['Ano de referência'], format='%Y')
    
    return df

def analise_pse2020():
    df = load_pse2020()

    # Alunos bairro
    alunos_por_bairro = df['Código do Núcleo PM'].value_counts().reset_index()
    alunos_por_bairro.columns = ['Bairro', 'Total de Alunos']
    alunos_por_bairro = alunos_por_bairro.sort_values(by='Total de Alunos', ascending=False)

    fig = px.bar(y = alunos_por_bairro['Bairro'], x = alunos_por_bairro['Total de Alunos'], text_auto = True, title = 'Total de Alunos por Bairro', orientation = 'h', 
                    labels = dict(y = 'Bairro', x = 'Total de Alunos'))
    fig.update_layout(title_text = 'Total de Alunos por Bairro', title_x = 0.4)
    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)
    
    st.subheader('Total de filhos ou enteados alunos da Passos Mágicos')

    st.write('No gráfico abaixo podemos ver a relação entre a quantidade total de filhos ou enteados no domícilio em relação ao número de alunos da Passos Mágicos.', )
    st.write('A partir dessa relação, conseguimos dimensionar visualmente pelo tamanho dos círculos a quantidade de cada um dos cenários e evidenciar através das cores, quais destes, todos os filhos ou enteados da casa, são alunos da Passos Mágicos')

    df_total_filhos_vs_total_passos = df.groupby(['Total de filhos ou enteados', 'Total de alunos Passos Mágicos'])['Código do domicilio'].count().reset_index()
    df_total_filhos_vs_total_passos.rename({'Código do domicilio': 'Quantidade de domicílios'}, inplace=True, axis=1)
    df_total_filhos_vs_total_passos['Todos são alunos da Passos Mágicos'] = df_total_filhos_vs_total_passos['Total de filhos ou enteados'] == df_total_filhos_vs_total_passos['Total de alunos Passos Mágicos']
    df_total_filhos_vs_total_passos['Todos são alunos da Passos Mágicos'] = df_total_filhos_vs_total_passos['Todos são alunos da Passos Mágicos'].replace(True, 'Sim').replace(False, 'Não')
    
    fig = px.scatter(df_total_filhos_vs_total_passos, x="Total de filhos ou enteados", y="Total de alunos Passos Mágicos", size="Quantidade de domicílios",
           color='Todos são alunos da Passos Mágicos', log_x=True, size_max=60, color_discrete_map={
                "Sim": "green",
                "Não": "blue"})

    fig.update_layout(title_text = 'Total de filhos ou enteados alunos da Passos Mágicos', title_x = 0.2)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Gráfico de dispersão para total de moradores em relação à renda per capita
    st.subheader('Renda Per Capita em relação ao Total de Moradores')
    fig2 = px.scatter(df, x='Total de moradores', y='Renda per capita', title='Renda Per Capita em relação ao Total de Moradores')
    st.plotly_chart(fig2)

    # Gráfico de violino para distribuição da idade do responsável por cor ou raça
    st.subheader('Distribuição da Idade do Responsável por Quantidade de Filhos ou Enteados')
    fig7 = px.violin(df, x='Total de filhos ou enteados', y='Idade do responsável', title='Distribuição da Idade do Responsável por Total de Filhos ou Enteados')
    st.plotly_chart(fig7)

    # Criar um DataFrame para o gráfico de calor
    heatmap_data = df.groupby(['Renda per capita', 'Total de alunos Passos Mágicos']).size().reset_index(name='count')

    # Criar o gráfico de calor
    st.subheader('Relação entre Renda Per Capita e Quantidade de Alunos Passos Mágicos')
    fig15 = px.density_heatmap(heatmap_data, x='Renda per capita', y='Total de alunos Passos Mágicos', z='count',
                                title='Relação entre Renda Per Capita e Quantidade de Alunos Passos Mágicos',
                                labels={'Renda per capita': 'Renda per capita', 'Total de alunos Passos Mágicos': 'Total de Alunos Passos Mágicos'})
    
    # Configurar a escala de cores do gráfico
    fig15.update_traces(colorscale='Viridis', reversescale=True)

    st.plotly_chart(fig15)

    # Gráfico de dispersão para renda per capita em relação ao número de filhos ou enteados no domicílio
    st.subheader('Renda Per Capita em relação ao Número de Filhos ou Enteados no Domicílio')
    fig12 = px.scatter(df, x='Total de filhos ou enteados', y='Renda per capita', title='Renda Per Capita em relação ao Número de Filhos ou Enteados no Domicílio')
    st.plotly_chart(fig12)

    # Gráfico de pizza para distribuição do tipo de domicílio
    st.subheader('Distribuição do Tipo de Domicílio')
    tipo_domicilio_counts = df['Tipo do domicílio'].value_counts()
    fig14 = px.pie(names=tipo_domicilio_counts.index, values=tipo_domicilio_counts.values, title='Distribuição do Tipo de Domicílio')
    st.plotly_chart(fig14)

    # Gráfico de barras: Média de Renda Per Capita por categoria de acesso à internet
    st.subheader('Média de Renda Per Capita por Categoria de Acesso à Internet')
    renda_por_internet = df.groupby('Tem acesso à internet?')['Renda per capita'].mean()
    fig18 = px.bar(renda_por_internet, x=renda_por_internet.index, y=renda_por_internet.values, color=renda_por_internet.index,
                    title='Média de Renda Per Capita por Categoria de Acesso à Internet',
                    labels={'x': 'Acesso à Internet', 'y': 'Média de Renda Per Capita'})
    st.plotly_chart(fig18)

    # Gráfico de barras: Total de Alunos Passos Mágicos por faixa de pobreza
    st.subheader('Total de Alunos Passos Mágicos por Faixa de Pobreza')
    alunos_por_pobreza = df.groupby('Linhas pobreza')['Total de alunos Passos Mágicos'].sum()
    fig19 = px.bar(alunos_por_pobreza, x=alunos_por_pobreza.index, y=alunos_por_pobreza.values, color=alunos_por_pobreza.index,
                    title='Total de Alunos Passos Mágicos por Faixa de Pobreza',
                    labels={'x': 'Faixa de Pobreza', 'y': 'Total de Alunos Passos Mágicos'})
    st.plotly_chart(fig19)