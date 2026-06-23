[README (1).md](https://github.com/user-attachments/files/29270135/README.1.md)
# 📊 Mercado de Trabalho em Dados — Análise de Salários (2020–2023)

Análise exploratória e dashboard interativo sobre salários de profissionais de dados pelo mundo, usando **Python, pandas, Seaborn e Streamlit**. O projeto cobre todo o ciclo: da exploração dos dados ao deploy de um app web público.

🔗 **[Acesse o dashboard interativo aqui](https://dashboard-salarios-dados-ntyd5wqwnejeqzab2hvd8x.streamlit.app/)**

---

## 🎯 Objetivo

Entender como variam os salários na área de dados de acordo com **senioridade, cargo, modalidade de trabalho, tamanho da empresa e localização**, e identificar tendências do mercado entre 2020 e 2023.

---

## 📁 Sobre os dados

- **Fonte:** Data Science Job Salaries (Kaggle)
- **Volume:** 3.755 registros, 11 colunas
- **Período:** 2020 a 2023
- **Observação:** salários convertidos para dólar (US$) para permitir comparação justa entre países.

---

## 🔍 Principais descobertas

- **A senioridade é o maior fator salarial:** o salário médio mais que dobra de Júnior (US$ 78k) a Executivo (US$ 195k).
- **Os cargos mais bem pagos são de liderança e especialização** (Tech Lead, Cloud Architect, Principal) — e não os cargos "genéricos" como eu imaginava no início.
- **O mercado está em forte ascensão:** o salário médio subiu cerca de 61% entre 2020 e 2023.
- **Um achado que me surpreendeu:** empresas de porte médio pagam, em média, mais do que as grandes.
- **Cuidado com amostras pequenas:** algumas categorias (como trabalho híbrido ou países específicos) têm poucos registros. Antes de tirar conclusões, investiguei o tamanho da amostra — uma preocupação que mantive em todo o projeto pra não afirmar o que o dado não sustenta.

---

## 🛠️ Etapas do projeto

1. **Coleta e carregamento** dos dados direto de uma URL pública.
2. **Exploração inicial** (estrutura, tipos, valores nulos, duplicatas).
3. **Tratamento e transformação** (tradução de categorias, criação de novas colunas).
4. **Análise exploratória (EDA)** com visualizações por senioridade, cargo, modalidade, país e tempo.
5. **Construção de um dashboard interativo** em Streamlit, com filtros e múltiplos gráficos.
6. **Deploy** público via Streamlit Community Cloud.

---

## 💻 Tecnologias utilizadas

- **Python** — linguagem principal
- **pandas** — manipulação e análise de dados
- **Seaborn / Matplotlib** — visualização de dados
- **Streamlit** — dashboard web interativo
- **Google Colab** — ambiente de análise

---

## 📂 Estrutura do repositório

```
├── app.py                  # dashboard interativo (Streamlit)
├── requirements.txt        # dependências do projeto
├── .streamlit/config.toml  # tema visual do dashboard
├── notebook_analise.ipynb  # análise exploratória completa
└── README.md               # este arquivo
```

---

## 🚀 Como executar localmente

```bash
# clonar o repositório
git clone https://github.com/matheussanchezsabbath-maker/dashboard-salarios-dados.git
cd dashboard-salarios-dados

# instalar dependências
pip install -r requirements.txt

# rodar o dashboard
streamlit run app.py
```

---

## 👤 Autor

**Matheus Mucci Sanchez**
[LinkedIn](https://www.linkedin.com/in/matheus-mucci-sanchez-aaba72385/) · [GitHub](https://github.com/matheussanchezsabbath-maker)
