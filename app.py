import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Salários em Dados",
    page_icon="📊",
    layout="wide",
)

VERDE = "#0F6E56"
PALETA = "crest"

# ----------------------------------------------------------------------
# CARREGAR OS DADOS (com cache pra não recarregar a cada clique)
# ----------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/Sujayketkar/Data-Science-Salaries/main/ds_salaries.csv"
    df = pd.read_csv(url)

    # traduções pra deixar legível
    mapa_senioridade = {"EN": "Júnior", "MI": "Pleno", "SE": "Sênior", "EX": "Executivo"}
    mapa_modalidade = {0: "Presencial", 50: "Híbrido", 100: "Remoto"}
    df["senioridade"] = df["experience_level"].map(mapa_senioridade)
    df["modalidade"] = df["remote_ratio"].map(mapa_modalidade)
    return df

df = carregar_dados()

# ----------------------------------------------------------------------
# CABEÇALHO
# ----------------------------------------------------------------------
st.title("📊 Mercado de Trabalho em Dados")
st.markdown("Análise de **3.755 salários** de profissionais de dados pelo mundo (2020–2023). "
            "Dados em dólar (US$). Fonte: *Data Science Job Salaries*.")
st.divider()

# ----------------------------------------------------------------------
# FILTROS (barra lateral)
# ----------------------------------------------------------------------
st.sidebar.header("Filtros")

senioridades = st.sidebar.multiselect(
    "Senioridade",
    options=df["senioridade"].unique(),
    default=df["senioridade"].unique(),
)

modalidades = st.sidebar.multiselect(
    "Modalidade",
    options=df["modalidade"].unique(),
    default=df["modalidade"].unique(),
)

# aplica os filtros
df_filtrado = df[
    (df["senioridade"].isin(senioridades)) &
    (df["modalidade"].isin(modalidades))
]

# segurança: se filtrar tudo e não sobrar nada
if df_filtrado.empty:
    st.warning("Nenhum dado para os filtros selecionados. Ajuste os filtros à esquerda.")
    st.stop()

# ----------------------------------------------------------------------
# CARTÕES DE INDICADORES (KPIs)
# ----------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Registros", f"{len(df_filtrado):,}".replace(",", "."))
col2.metric("Salário médio", f"US$ {round(df_filtrado['salary_in_usd'].mean()):,}")
col3.metric("Salário mediano", f"US$ {round(df_filtrado['salary_in_usd'].median()):,}")

st.divider()

# ----------------------------------------------------------------------
# GRÁFICOS — linha 1
# ----------------------------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Salário médio por senioridade")
    ordem = ["Júnior", "Pleno", "Sênior", "Executivo"]
    dados = df_filtrado.groupby("senioridade")["salary_in_usd"].mean().reindex(ordem).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=dados.index, y=dados.values, hue=dados.index, palette=PALETA, legend=False, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Salário médio (US$)")
    sns.despine()
    st.pyplot(fig)

with col_b:
    st.subheader("Top 10 cargos por salário médio")
    top_cargos = df_filtrado.groupby("job_title")["salary_in_usd"].mean().nlargest(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=top_cargos.values, y=top_cargos.index, hue=top_cargos.index, palette=PALETA, legend=False, ax=ax)
    ax.set_xlabel("Salário médio (US$)")
    ax.set_ylabel("")
    sns.despine()
    st.pyplot(fig)

# ----------------------------------------------------------------------
# GRÁFICOS — linha 2
# ----------------------------------------------------------------------
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Evolução do salário médio (2020–2023)")
    salario_ano = df_filtrado.groupby("work_year")["salary_in_usd"].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(x=salario_ano.index, y=salario_ano.values, marker="o", color=VERDE, linewidth=2.5, ax=ax)
    ax.set_xlabel("Ano")
    ax.set_ylabel("Salário médio (US$)")
    ax.set_xticks(salario_ano.index)
    sns.despine()
    st.pyplot(fig)

with col_d:
    st.subheader("Salário médio por modalidade")
    salario_mod = df_filtrado.groupby("modalidade")["salary_in_usd"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=salario_mod.index, y=salario_mod.values, hue=salario_mod.index, palette=PALETA, legend=False, ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Salário médio (US$)")
    sns.despine()
    st.pyplot(fig)
    st.caption("⚠️ Atenção: o número de registros varia muito entre modalidades "
               "(ex.: 'Híbrido' tem poucos dados), então compare com cautela.")

# ----------------------------------------------------------------------
# RODAPÉ
# ----------------------------------------------------------------------
st.divider()
st.caption("Projeto de análise de dados • Python, pandas, Seaborn e Streamlit")
