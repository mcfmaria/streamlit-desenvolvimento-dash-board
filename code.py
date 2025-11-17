import streamlit as st
import pandas as pd
import altair as alt
from pymongo import MongoClient

# ----------------------------------------------------
# CONFIGURAÇÃO
# ----------------------------------------------------
st.set_page_config(page_title="Dashboard Serviços", layout="wide")

# 🔐 SENHA DO SISTEMA
PASSWORD = "F7F899@"   # <-- TROQUE AQUI

# 🔌 CONEXÃO COM O MONGO DB ATLAS
MONGO_URI = "mongodb+srv://mcfwork07_db_user:PedroM@bel292801@dadoups.bmoszxu.mongodb.net/?appName=dadoups"
DB_NAME = "Trabalho"
COLLECTION_NAME = "ups"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# ----------------------------------------------------
# FUNÇÃO DE LOGIN
# ----------------------------------------------------
def check_password():
    with st.sidebar:
        st.title("🔐 Login")
        pwd = st.text_input("Digite a senha", type="password")
        if pwd == PASSWORD:
            return True
        elif pwd:
            st.error("Senha incorreta!")
    return False

if not check_password():
    st.stop()


# ----------------------------------------------------
# TÍTULO
# ----------------------------------------------------
st.title("📊 Dashboard de Serviços (MongoDB)")


# ----------------------------------------------------
# PEGAR OS DADOS DIRETO DO MONGO
# ----------------------------------------------------
st.info("Buscando dados no MongoDB Atlas...")

dados = list(collection.find({}, {"_id": 0}))  # remove _id

if not dados:
    st.error("❌ Nenhum dado encontrado no MongoDB!")
    st.stop()

df = pd.DataFrame(dados)

st.subheader("Pré-visualização dos dados do banco")
st.dataframe(df)


# ----------------------------------------------------
# CARDS
# ----------------------------------------------------
media_total = df["MÉDIA"].mean()
total_turnos = df["TURNOS"].sum()
total_servicos = df["TOTAL"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("📌 Média Geral", f"{media_total:.2f}")
col2.metric("👷 Total de Turnos", int(total_turnos))
col3.metric("🧾 Total de Serviços", int(total_servicos))


# ----------------------------------------------------
# GRÁFICO 1: CLASSE por PREFIXO
# ----------------------------------------------------
st.subheader("Distribuição de CLASSE por PREFIXO")

grafico1 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("PREFIXO:N", title="PREFIXO"),
        y=alt.Y("count():Q", title="Quantidade"),
        color=alt.Color("CLASSE:N", title="CLASSE")
    )
    .properties(height=350)
)

st.altair_chart(grafico1, use_container_width=True)


# ----------------------------------------------------
# GRÁFICO 2: Donut da CLASSE total
# ----------------------------------------------------
st.subheader("Classe total")

df_classe = df["CLASSE"].value_counts().reset_index()
df_classe.columns = ["CLASSE", "QTD"]

donut = (
    alt.Chart(df_classe)
    .mark_arc(innerRadius=70)
    .encode(
        theta="QTD:Q",
        color="CLASSE:N"
    )
    .properties(height=300)
)

st.altair_chart(donut, use_container_width=True)


# ----------------------------------------------------
# GRÁFICO 3: Equipes por mês
# ----------------------------------------------------
st.subheader("Equipes por Mês")

grafico3 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="MÊS:N",
        y="EQUIPE:Q",
        color="MÊS:N"
    )
    .properties(height=320)
)

st.altair_chart(grafico3, use_container_width=True)
