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

    df = pd.read_csv(csv_string_io, sep=';', decimal=".")
    # df['IDADE_ALUNO_2020'] = df['IDADE_ALUNO_2020'].fillna(0)

    return df

def analise_pede():
    df = load_pede_data()
    st.write('Em 2016 a ONG transformava as vidas de 70 alunos, hoje a Passos Mágicos tem impactado as vidas das crianças em um número crescente atingindo um total de 1100 em 2023, o que corresponde cerca de 14x mais o número em 2016.', )

    df['2020'] = df['FASE_TURMA_2020'].apply(lambda x: 1 if pd.notna(x) else 0)
    df['2021'] = df['TURMA_2021'].apply(lambda x: 1 if pd.notna(x) else 0)
    df['2022'] = df['TURMA_2022'].apply(lambda x: 1 if pd.notna(x) else 0)

    alunos_por_ano = df[['2020', '2021', '2022']].sum().reset_index()
    alunos_por_ano.columns = ['index', 'values']
    fig = px.bar(alunos_por_ano, x="index", y="values", title='Quantidade de Alunos por Ano', labels=dict(values="Quantidade de Alunos", index="Ano"))
    fig.update_xaxes(tickvals=alunos_por_ano['index'])
    fig.update_layout(title_text = 'Quantidade de Alunos por Ano')

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.write('Cada vez mais as crianças poderão mudar o rumo da suas vidas, traçando um futuro melhor através da educação.')

    # Distribuição de Notas por Disciplina em 2022
    st.subheader('Aulas')
    st.write('A Associação Passos Mágicos oferece aulas de alfabetização, língua portuguesa e matemática para crianças e adolescentes, de 7 a 17 anos, que sejam baixa renda e moradores do município de Embu-Guaçu. Os alunos são divididos por nível de conhecimento, determinado por meio de uma prova de sondagem que é realizada ao ingressarem na Passos Mágicos, e são inseridos em turmas que variam da alfabetização até o nível 8.')

    df_media_notas = df[['NOTA_PORT_2022', 'NOTA_MAT_2022', 'NOTA_ING_2022']].mean().reset_index()
    df_media_notas.columns = ['Disciplina', 'Média']
    df_media_notas = df_media_notas.replace('NOTA_PORT_2022', 'Português 2022')
    df_media_notas = df_media_notas.replace('NOTA_MAT_2022', 'Matemática 2022')
    df_media_notas = df_media_notas.replace('NOTA_ING_2022', 'Inglês 2022')
    st.write()
    fig4 = px.bar(df_media_notas, x='Disciplina', y='Média', color='Disciplina', title='Média de Notas por Disciplina (2022)')
    st.plotly_chart(fig4)

    # Desempenho dos Bolsistas em 2022
    df_media_notas_bolsistas = df.groupby('BOLSISTA_2022').mean(['NOTA_PORT_2022', 'NOTA_MAT_2022', 'NOTA_ING_2022'])[['NOTA_PORT_2022', 'NOTA_MAT_2022', 'NOTA_ING_2022']]

    nota_port = df_media_notas_bolsistas['NOTA_PORT_2022'].reset_index()
    nota_port['Disciplina'] = 'Português'
    nota_port.columns = ['Bolsista', 'Nota', 'Disciplina']

    nota_mat = df_media_notas_bolsistas['NOTA_MAT_2022'].reset_index()
    nota_mat['Disciplina'] = 'Matemática'
    nota_mat.columns = ['Bolsista', 'Nota', 'Disciplina']

    nota_ing = df_media_notas_bolsistas['NOTA_ING_2022'].reset_index()
    nota_ing['Disciplina'] = 'Inglês'
    nota_ing.columns = ['Bolsista', 'Nota', 'Disciplina']

    df_media_notas_disciplina = pd.concat([nota_port, nota_mat, nota_ing])

    fig = px.bar(df_media_notas_disciplina, x='Disciplina', y='Nota', color='Bolsista', barmode='group',
             labels={'Nota': 'Nota Média', 'Disciplina': 'Disciplina', 'Bolsista': 'Bolsista'},
             title='Nota Média por Disciplina e Status de Bolsista')
    st.plotly_chart(fig)

    st.write('Com as aulas, além da bagagem cultural oferecida, a partir de atividades estruturadas para que haja melhor aproveitamento do conteúdo, o acompanhamento torna possível que os alunos se capacitem para superar suas dificuldades acadêmicas e aprimorar suas habilidades.')
    st.write('Em cada uma das disciplinas são apresentadas atividades que instiguem as crianças e os adolescentes a acessarem sua criatividade e que despertem o interesse pela busca do saber. Dentre elas, atividades complementares pedagógicas, envolvendo desde o exercício da leitura e da escrita, até o desenvolvimento de projetos artísticos que possibilitem um contato mais dinâmico com as matérias.')


    # Desempenho por Nível Ideal em 2022
    st.subheader('Indicador de Autoavaliação - IAA')
    st.write('Durante a jornada do aluno na associação e além do conteúdo acadêmico, a associação busca entender como o estudando se autoavalia. Dentre as várias formas de acompanhar a criança, a IAA (Indicador de Autoavaliação) traz por meio dos seus resultados, respostas sobre os aspectos da vida do aluno e da sua experiência cotidiana, com questões sobre os sentimentos do estudando em relação a si mesmo, sobre os estudos, sobre sua vida familiar, relação com os amigos, sobre a Passos mágicos e em relação aos professores.')

    fig7 = px.bar(df, x='NIVEL_IDEAL_2022', y='IAA_2022', color='NIVEL_IDEAL_2022', title='Desempenho (IAA_2022) em 2022 por Nível Ideal')
    st.plotly_chart(fig7)


    # Correlação entre Desempenho e Recomendações da Equipe em 2022
    st.subheader('Indicador Psicopedagógico - IPP')
    st.write('O IPP é uma avaliação realizada educadores e psicopedagogos para caracterizar o desenvolvimento cognitivo, emocional, comportamental e da socialização do aluno no seu processo de aprendizado dentro do Programa de Aceleração de Conhecimento.')
    st.write('As questões avaliam se o aluno possui adequação e autonomia, uma boa adequação geral, se possui interações disfuncionais ou se está em atendimento terapêutico. ')

    rec_equipe_1 = df[['REC_EQUIPE_1_2021']]
    rec_equipe_1['Equipe'] = 'Equipe 1 2021'
    rec_equipe_1.columns = ['Recomendação', 'Equipe']

    rec_equipe_2 = df[['REC_EQUIPE_2_2021']]
    rec_equipe_2['Equipe'] = 'Equipe 2 2021'
    rec_equipe_2.columns = ['Recomendação', 'Equipe']

    rec_equipe_3 = df[['REC_EQUIPE_3_2021']]
    rec_equipe_3['Equipe'] = 'Equipe 3 2021'
    rec_equipe_3.columns = ['Recomendação', 'Equipe']

    rec_equipe_4 = df[['REC_EQUIPE_4_2021']]
    rec_equipe_4['Equipe'] = 'Equipe 4 2021'
    rec_equipe_4.columns = ['Recomendação', 'Equipe']

    rec_equipes = pd.concat([rec_equipe_1, rec_equipe_2, rec_equipe_3, rec_equipe_4]).reset_index()
    rec_equipes_agrupado = rec_equipes.groupby(['Recomendação', 'Equipe']).count()['index'].reset_index()

    recomendacao_lista = rec_equipes_agrupado['Recomendação'].unique().tolist()
    recomendacao_lista.append('Todas')
    recomendacao_selecionada = st.selectbox('Selecione uma opção:', recomendacao_lista, index=(len(recomendacao_lista)-1))

    if (recomendacao_selecionada != 'Todas'):
        rec_equipes_agrupado_filtrado = rec_equipes_agrupado[rec_equipes_agrupado['Recomendação'] == recomendacao_selecionada]
    else:
        rec_equipes_agrupado_filtrado = rec_equipes_agrupado

    fig = px.bar(rec_equipes_agrupado_filtrado, x='Recomendação', y='index', color='Equipe', barmode='group',
             labels={'y': 'Quantidade de Alunos'},
             title='Recomendação dos Alunos por Equipe (2021)')
    st.plotly_chart(fig)
    st.write('As recomendações finais sugerem se o estudante deveria ser promovido de fase e indicado para bolsas, se deveria ser mantido na fase atual e indicado para bolsas, se deveria ser promovido de fase sem indicação para bolsas, se deveria ser mantido na fase e sem indicação para bolsa ou se deveria ser recuado de fase.')

    #Calcular a porcentagem de alunos que atingiram o ponto de virada em cada ano

    st.subheader('Indicador do Ponto de Virada - IPV')
    st.write('Estágio do desenvolvimento do estudante para demonstrar de forma ativa, por meio da sua trajetória dentro da associação, que o aluno está consciente da importância da educação, do valor de saber e da importância de aprender.')
    st.write('A avaliação é realizada pelos pedagogos e professores, as questões de avaliação consideram a integração do aluno na associação, desenvolvimento emocional do aluno e potencial acadêmico.')
    st.write('Cada elemento avaliado possui pesos e valores, o aluno é avaliado se possui desempenho positivo, suficiente, insuficiente e se apresenta dificuldades.')

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
    fig.update_layout(title_text = 'Alunos que atingiram o Ponto de Virada por Ano')
    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

    st.write('O indicador não se trata de um ponto de chegada, mas que o aluno está apto para iniciar a transformação na vida por meio da educação. Sendo assim, podemos dizer que 1/3 dos alunos que ingressaram na associação puderam iniciar esta transformação. ')

