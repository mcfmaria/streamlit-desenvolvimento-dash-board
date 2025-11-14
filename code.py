import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------------------------------
# CONFIGURAÇÃO
# ----------------------------------------------------
st.set_page_config(page_title="Dashboard Serviços", layout="wide")

# SENHA DO SISTEMA
PASSWORD = "ln11Col13@"   # <-- TROQUE AQUI

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
st.title("📊 Dashboard de Serviços")

# ----------------------------------------------------
# UPLOAD DA PLANILHA
# ----------------------------------------------------
arquivo = st.file_uploader("Carregar planilha Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.subheader("Pré-visualização dos dados")
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
    # GRÁFICO 1: CLASSE por PREFIXO (barras empilhadas)
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
    # GRÁFICO 3: Média das equipes por mês
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
