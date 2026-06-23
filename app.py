import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Salários em Dados", page_icon="📊", layout="wide")

VERDE = "#1D9E75"
VERDE_ESCURO = "#0F6E56"
TEXTO = "#E8E6DF"
FUNDO = "#0E1512"
PALETA_VERDE = ["#9FE1CB", "#5DCAA5", "#1D9E75", "#0F6E56"]

plt.rcParams.update({
    "text.color": TEXTO, "axes.labelcolor": TEXTO,
    "xtick.color": TEXTO, "ytick.color": TEXTO,
    "axes.edgecolor": "#3A4A42", "axes.titlecolor": TEXTO,
})

def fundo_transparente(fig, ax):
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    sns.despine(ax=ax)

@st.cache_data
def carregar_dados():
    url = "https://raw.githubusercontent.com/Sujayketkar/Data-Science-Salaries/main/ds_salaries.csv"
    df = pd.read_csv(url)
    df["senioridade"] = df["experience_level"].map({"EN": "Júnior", "MI": "Pleno", "SE": "Sênior", "EX": "Executivo"})
    df["modalidade"] = df["remote_ratio"].map({0: "Presencial", 50: "Híbrido", 100: "Remoto"})
    df["tamanho"] = df["company_size"].map({"S": "Pequena", "M": "Média", "L": "Grande"})
    return df

df = carregar_dados()

ORDEM_SEN = ["Júnior", "Pleno", "Sênior", "Executivo"]
ORDEM_MOD = ["Presencial", "Híbrido", "Remoto"]
ORDEM_TAM = ["Pequena", "Média", "Grande"]

st.title("📊 Mercado de Trabalho em Dados")
st.markdown("Análise de **3.755 salários** de profissionais de dados pelo mundo (2020–2023). "
            "Valores em dólar (US$). Fonte: *Data Science Job Salaries*.")
st.divider()

st.sidebar.header("Filtros")
senioridades = st.sidebar.multiselect("Senioridade", df["senioridade"].unique(), default=list(df["senioridade"].unique()))
modalidades = st.sidebar.multiselect("Modalidade", df["modalidade"].unique(), default=list(df["modalidade"].unique()))
df_f = df[(df["senioridade"].isin(senioridades)) & (df["modalidade"].isin(modalidades))]

if df_f.empty:
    st.warning("Nenhum dado para os filtros selecionados. Ajuste os filtros à esquerda.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Registros", f"{len(df_f):,}".replace(",", "."))
c2.metric("Salário médio", f"US$ {round(df_f['salary_in_usd'].mean()):,}")
c3.metric("Salário mediano", f"US$ {round(df_f['salary_in_usd'].median()):,}")
st.divider()

# ---- linha 1 ----
ca, cb = st.columns(2)
with ca:
    st.subheader("Salário médio por senioridade")
    d = df_f.groupby("senioridade")["salary_in_usd"].mean().reindex(ORDEM_SEN).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=d.index, y=d.values, hue=d.index, palette=PALETA_VERDE, legend=False, ax=ax)
    for i, v in enumerate(d.values):
        ax.text(i, v, f"US$ {v:,.0f}", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_xlabel(""); ax.set_ylabel("Salário médio (US$)"); ax.margins(y=0.15)
    fundo_transparente(fig, ax); st.pyplot(fig)

with cb:
    st.subheader("Top 10 cargos por salário médio")
    tc = df_f.groupby("job_title")["salary_in_usd"].mean().nlargest(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=tc.values, y=tc.index, color=VERDE, ax=ax)
    ax.set_xlabel("Salário médio (US$)"); ax.set_ylabel("")
    fundo_transparente(fig, ax); st.pyplot(fig)

# ---- linha 2 ----
cc, cd = st.columns(2)
with cc:
    st.subheader("Evolução do salário médio (2020–2023)")
    sa = df_f.groupby("work_year")["salary_in_usd"].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(x=sa.index, y=sa.values, marker="o", color=VERDE, linewidth=2.5, ax=ax)
    for ano, v in sa.items():
        ax.text(ano, v, f"  US$ {v:,.0f}", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_xlabel("Ano"); ax.set_ylabel("Salário médio (US$)"); ax.set_xticks(sa.index); ax.margins(y=0.15)
    fundo_transparente(fig, ax); st.pyplot(fig)

with cd:
    st.subheader("Salário médio por modalidade")
    sm = df_f.groupby("modalidade")["salary_in_usd"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=sm.index, y=sm.values, color=VERDE, ax=ax)
    for i, v in enumerate(sm.values):
        ax.text(i, v, f"US$ {v:,.0f}", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_xlabel(""); ax.set_ylabel("Salário médio (US$)"); ax.margins(y=0.15)
    fundo_transparente(fig, ax); st.pyplot(fig)
    st.caption("⚠️ 'Híbrido' tem poucos registros — compare com cautela.")

# ---- linha 3 ----
ce, cf = st.columns(2)
with ce:
    st.subheader("Salário médio por tamanho de empresa")
    dt = df_f.groupby("tamanho")["salary_in_usd"].mean().reindex(ORDEM_TAM).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=dt.index, y=dt.values, color=VERDE, ax=ax)
    for i, v in enumerate(dt.values):
        ax.text(i, v, f"US$ {v:,.0f}", ha="center", va="bottom", color=TEXTO, fontsize=9)
    ax.set_xlabel(""); ax.set_ylabel("Salário médio (US$)"); ax.margins(y=0.15)
    fundo_transparente(fig, ax); st.pyplot(fig)

with cf:
    st.subheader("Proporção de registros por senioridade")
    cont = df_f["senioridade"].value_counts().reindex(ORDEM_SEN).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    wedges, texts, autotexts = ax.pie(
        cont.values, labels=cont.index, autopct="%1.0f%%",
        colors=PALETA_VERDE, wedgeprops={"width": 0.45, "edgecolor": FUNDO},
        textprops={"color": TEXTO, "fontsize": 10})
    for at in autotexts:
        at.set_color("white"); at.set_fontsize(9)
    ax.set_aspect("equal"); fig.patch.set_alpha(0)
    st.pyplot(fig)

# ---- linha 4: mapa de calor ----
cg, ch = st.columns([3, 2])
with cg:
    st.subheader("Salário médio: senioridade × modalidade")
    pivot = df_f.pivot_table(index="senioridade", columns="modalidade",
                             values="salary_in_usd", aggfunc="mean").reindex(index=ORDEM_SEN, columns=ORDEM_MOD)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="crest", cbar=False,
                linewidths=1, linecolor=FUNDO, annot_kws={"size": 9}, ax=ax)
    ax.set_xlabel(""); ax.set_ylabel(""); fig.patch.set_alpha(0)
    st.pyplot(fig)
    st.caption("Cada célula = salário médio (US$) da combinação. Células com poucos registros podem oscilar.")
with ch:
    st.subheader("Principais descobertas")
    st.markdown(
        "- O salário **mais que dobra** de Júnior a Executivo.\n"
        "- Os cargos do topo são de **liderança e especialização** (Tech Lead, Architect).\n"
        "- O salário médio **subiu ~61%** entre 2020 e 2023.\n"
        "- Diferenças entre modalidades podem refletir **amostra**, não causa."
    )

st.divider()
st.caption("Projeto de análise de dados • Python, pandas, Seaborn e Streamlit")
