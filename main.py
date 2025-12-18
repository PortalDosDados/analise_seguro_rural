# Importação das bibliotecas necessárias
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Carregamento dos dados
df = pd.read_csv('C:/Users/dione/Documents/GitHub/analise_seguro_rural/assets/dados_abertos_psr_2006a2015.csv', encoding = 'latin1', sep=';')

# Configuração da página
st.set_page_config(page_title='Análise de Dados PSR 2006-2015', layout='wide')
st.title('Análise de Dados Abertos PSR 2006-2015')
st.markdown('Exploração interativa dos dados abertos do PSR de 2006 a 2015.')

# Exibição dos dados brutos
st.subheader('Dados Brutos')
st.dataframe(df.head())



# Gráfico de Barras Horizontais 1: Distribuição dos Tipos NM_CULTURA_GLOBAL
st.subheader('Distribuição dos Tipos de Cultura Global')

# Cria DataFrame com categorias e suas contagens
df_culturas = df['NM_CULTURA_GLOBAL'].value_counts().reset_index()
df_culturas.columns = ['Tipo de Cultura Global', 'Quantidade']

# Gráfico de barras horizontais
fig2 = px.bar(
    data_frame=df_culturas,
    y='Tipo de Cultura Global',   # categorias no eixo Y
    x='Quantidade',               # contagem no eixo X
    orientation='h',
    title='Distribuição dos Tipos de Cultura Global (Barras Horizontais)',
    labels={'Tipo de Cultura Global': 'Tipo de Cultura Global', 'Quantidade': 'Quantidade'},
    color_discrete_sequence=['#EF553B']
)

# Ajusta o layout do gráfico
fig2.update_layout(yaxis={'categoryorder':'total ascending'},  # Ordena categorias pela contagem
                   xaxis_title='Quantidade',
                     yaxis_title='Tipo de Cultura Global')

# Rotula os rótulos do eixo Y para melhor legibilidade
fig2.update_yaxes(tickangle=0, tickfont=dict(size=10))




# Exibe no Streamlit
st.plotly_chart(fig2, use_container_width=True)


