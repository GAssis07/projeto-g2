# ====================================
# Projeto G2 - Dashboard Streamlit
# Análise da Qualidade do Ar no Brasil
# ====================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ---------------------------------------
# Configurações da página
# ---------------------------------------

st.set_page_config(
    page_title="Qualidade do Ar no Brasil",
    page_icon="🌎",
    layout="wide"
)

sns.set_style("whitegrid")


# ---------------------------------------
# Carregamento dos dados
# ---------------------------------------

@st.cache_data
def carregar_dados():

    df = pd.read_csv(
        "dados/simulacao_qualidade_ar_brasil.csv"
    )

    df["data"] = pd.to_datetime(df["data"])

    return df


df = carregar_dados()


# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.title("Filtros")

regioes = st.sidebar.multiselect(
    "Selecione Região:",
    options=df["regiao"].unique(),
    default=df["regiao"].unique()
)

cidades = st.sidebar.multiselect(
    "Selecione Cidade:",
    options=df["cidade"].unique(),
    default=df["cidade"].unique()
)

anos = st.sidebar.multiselect(
    "Selecione Ano:",
    options=sorted(df["ano"].unique()),
    default=sorted(df["ano"].unique())
)

# Aplicando filtros

df_filtrado = df[
    (df["regiao"].isin(regioes)) &
    (df["cidade"].isin(cidades)) &
    (df["ano"].isin(anos))
]


# ---------------------------------------
# Título
# ---------------------------------------

st.title("🌎 Dashboard — Qualidade do Ar no Brasil")

st.markdown("""

Este projeto analisa indicadores ambientais relacionados à qualidade do ar em cidades brasileiras.

Objetivos:

- Identificar padrões de poluição
- Avaliar indicadores ambientais
- Analisar tendências temporais
- Apoiar tomadas de decisão

---
""")


# ---------------------------------------
# KPIs
# ---------------------------------------

st.subheader("📊 Indicadores Principais")

col1,col2,col3,col4=st.columns(4)

media_iqa = round(
    df_filtrado["indice_qualidade_ar"].mean(),2
)

pm25 = round(
    df_filtrado["pm25"].mean(),2
)

temperatura = round(
    df_filtrado["temperatura_media"].mean(),2
)

cidades_total = (
    df_filtrado["cidade"].nunique()
)


with col1:
    st.metric(
        "Média IQA",
        media_iqa
    )

with col2:
    st.metric(
        "PM2.5 Médio",
        pm25
    )

with col3:
    st.metric(
        "Temperatura Média",
        temperatura
    )

with col4:
    st.metric(
        "Cidades Monitoradas",
        cidades_total
    )


st.divider()


# ---------------------------------------
# Seção gráficos
# ---------------------------------------

st.subheader("📈 Visualizações")


col1,col2=st.columns(2)


# gráfico 1

with col1:

    fig, ax = plt.subplots()

    media_regiao=(
        df_filtrado
        .groupby("regiao")["indice_qualidade_ar"]
        .mean()
        .sort_values()
    )

    sns.barplot(
        x=media_regiao.index,
        y=media_regiao.values,
        ax=ax
    )

    plt.xticks(rotation=45)

    plt.title(
        "IQA Médio por Região"
    )

    st.pyplot(fig)



# gráfico 2

with col2:

    fig, ax = plt.subplots()

    sns.boxplot(
        data=df_filtrado,
        x="regiao",
        y="pm25",
        ax=ax
    )

    plt.xticks(rotation=45)

    plt.title(
        "Distribuição PM2.5"
    )

    st.pyplot(fig)



st.divider()


# ---------------------------------------
# Evolução temporal
# ---------------------------------------

st.subheader(
    "📉 Evolução Temporal"
)

serie = (
    df_filtrado
    .groupby("ano")
    ["indice_qualidade_ar"]
    .mean()
)

fig, ax = plt.subplots()

plt.plot(
    serie.index,
    serie.values
)

plt.xlabel("Ano")

plt.ylabel("IQA")

plt.title(
    "Evolução do Índice de Qualidade do Ar"
)

st.pyplot(fig)


st.divider()


# ---------------------------------------
# Correlação
# ---------------------------------------

st.subheader(
    "🔥 Correlação entre Variáveis"
)

colunas_numericas = (
    df_filtrado.select_dtypes(
        include=np.number
    )
)

corr = colunas_numericas.corr()

fig, ax = plt.subplots(
    figsize=(12,8)
)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

st.pyplot(fig)


st.divider()


# ---------------------------------------
# Tabela
# ---------------------------------------

st.subheader(
    "📄 Dados filtrados"
)

st.dataframe(
    df_filtrado,
    use_container_width=True
)


st.divider()


# ---------------------------------------
# Interpretação textual
# ---------------------------------------

st.subheader(
    "📝 Interpretação dos resultados"
)

cidade_critica = (
    df_filtrado.groupby(
        "cidade"
    )["indice_qualidade_ar"]
    .mean()
    .idxmax()
)

st.write(f"""

- A média atual do índice de qualidade do ar é **{media_iqa}**.

- A cidade com maior índice médio de poluição foi **{cidade_critica}**.

- O PM2.5 médio observado foi **{pm25}**.

- A matriz de correlação permite identificar relações entre variáveis ambientais.

""")


st.divider()


# ---------------------------------------
# Conclusão
# ---------------------------------------

st.subheader(
    "🎯 Conclusão Executiva"
)

st.success("""

Os resultados obtidos demonstram que a qualidade do ar não apresenta comportamento homogêneo entre as regiões brasileiras, existindo diferenças significativas nos indicadores ambientais analisados. A comparação entre regiões permitiu identificar localidades com maiores índices médios de poluição, enquanto a análise da distribuição do PM2.5 evidenciou variações relevantes entre cidades.

A evolução temporal dos indicadores sugere padrões que podem representar mudanças ambientais ao longo do período analisado, permitindo identificar tendências de crescimento ou redução dos níveis de poluentes. A análise de correlação também possibilitou compreender possíveis relações entre fatores ambientais e a qualidade do ar.

Dessa forma, o dashboard se apresenta como uma ferramenta de apoio à análise exploratória de dados ambientais, fornecendo informações relevantes para monitoramento, planejamento urbano e formulação de políticas públicas voltadas à sustentabilidade e à saúde da população.


""")
