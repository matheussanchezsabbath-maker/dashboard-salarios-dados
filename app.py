import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------------------
st.set_page_config(page_title="Salários em Dados", page_icon="📊", layout="wide")

# cores do tema
VERDE = "#1D9E75"
VERDE_ESCURO = "#0F6E56"
TEXTO = "#E8E6DF"
PALETA_VERDE = ["#9FE1CB", "#5DCAA5", "#1D9E75", "#0F6E56"]

# estilo escuro padrão para todos os gráficos
plt.rcParams.update({
    "text.color": TEXTO,
    "axes.labelcolor": TEXTO,
    "xtick.color": TEXTO,
    "ytick.color": TEXTO,
    "axes.edgecolor": "#3A4A42",
    "axes.titlecolor": TEXTO,
})

def fundo_transparente(fig, ax):
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    sns.despine(ax=ax)

# ----------------------------------------------------------------------
# CARREGAR OS DADOS
# ----------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/Sujayketkar/Data-Science-Salaries/main/ds_salaries.csv"
    df = pd.read_csv(url)
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
            "Valores em dólar (US$). Fonte: *Data Science Job Salaries*.")
st.divider()

# ----------------------------------------------------------------------
# FILTROS
# ----------------------------------------------------------------------
st.sidebar.header("Filtros")
senioridades = st.sidebar.multiselect("Senioridade", df["senioridade"].unique(), default=list(df["senioridade"].unique()))
modalidades = st.sidebar.multiselect("Modalidade", df["modalidade"].unique(), default=list(df["modalidade"].unique()))

df_f = df[(df["senioridade"].isin(senioridades)) & (df["modalidade"].isin(modalidades))]

if df_f.empty:
    st.warning("Nenhum dado para os filtros selecionados. Ajuste os filtros à esquerda.")
    st.stop()

# ----------------------------------------------------------------------
# KPIs
# ----------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Registros", f"{len(df_f):,}".replace(",", "."))
c2.metric("Salário médio", f"US$ {round(df_f['salary_in_usd'].mean()):,}")
c3.metric("Salário mediano", f"US$ {round(df_f['salary_in_usd'].median()):,}")
st.divider()

# ----------------------------------------------------------------------
# GRÁFICOS — linha 1
# ----------------------------------------------------------------------
ca, cb = st.columns(2)

with ca:
    st.subheader("Salário médio por senioridade")
    ordem = ["Júnior", "Pleno", "Sênior", "Executivo"]
    dados = df_f.groupby("senioridade")["salary_in_usd"].mean().reindex(ordem).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=dados.index, y=dados.values, hue=dados.index, palette=PALETA_VERDE, legend=False, ax=ax)
    for i, v in enumerate(dados.values):
        ax.text(i, v, f"US$ {v:,.0f}", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_xlabel(""); ax.set_ylabel("Salário médio (US$)")
    ax.margins(y=0.15)
    fundo_transparente(fig, ax)
    st.pyplot(fig)

with cb:
    st.subheader("Top 10 cargos por salário médio")
    top_cargos = df_f.groupby("job_title")["salary_in_usd"].mean().nlargest(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=top_cargos.values, y=top_cargos.index, color=VERDE, ax=ax)
    ax.set_xlabel("Salário médio (US$)"); ax.set_ylabel("")
    fundo_transparente(fig, ax)
    st.pyplot(fig)

# ----------------------------------------------------------------------
# GRÁFICOS — linha 2
# ----------------------------------------------------------------------
cc, cd = st.columns(2)

with cc:
    st.subheader("Evolução do salário médio (2020–2023)")
    salario_ano = df_f.groupby("work_year")["salary_in_usd"].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(x=salario_ano.index, y=salario_ano.values, marker="o", color=VERDE, linewidth=2.5, ax=ax)
    for ano, v in salario_ano.items():
        ax.text(ano, v, f"  US$ {v:,.0f}", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_xlabel("Ano"); ax.set_ylabel("Salário médio (US$)")
    ax.set_xticks(salario_ano.index)
    ax.margins(y=0.15)
    fundo_transparente(fig, ax)
    st.pyplot(fig)

with cd:
    st.subheader("Salário médio por modalidade")
    salario_mod = df_f.groupby("modalidade")["salary_in_usd"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=salario_mod.index, y=salario_mod.values, color=VERDE, ax=ax)
    for i, v in enumerate(salario_mod.values):
        ax.text(i, v, f"US$ {v:,.0f}", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_xlabel(""); ax.set_ylabel("Salário médio (US$)")
    ax.margins(y=0.15)
    fundo_transparente(fig, ax)
    st.pyplot(fig)
    st.caption("⚠️ O número de registros varia muito entre modalidades "
               "(ex.: 'Híbrido' tem poucos dados), então compare com cautela.")

# ----------------------------------------------------------------------
# RODAPÉ
# ----------------------------------------------------------------------
st.divider()
st.caption("Projeto de análise de dados • Python, pandas, Seaborn e Streamlit")
