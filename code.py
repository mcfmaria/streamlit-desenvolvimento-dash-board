import streamlit as st
import pandas as pd
import altair as alt
import json
from io import StringIO

# -------------------------
# Config
# -------------------------
st.set_page_config(page_title="Dashboard Serviços (JSON)", layout="wide")
PASSWORD = "F7F899@"   # <-- mantenha ou troque

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

st.title("📊 Dashboard de Serviços (usando dados.json)")

# -------------------------
# Função: carregar JSON local ou via upload
# -------------------------
def load_json_from_file(path="dados.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Erro ao ler {path}: {e}")
        return None

def load_json_from_uploader(uploaded_file):
    try:
        # uploaded_file é um BytesIO; ler como texto
        s = StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = json.load(s)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Erro ao ler JSON enviado: {e}")
        return None

# Tenta carregar dados.json local
df = load_json_from_file("dados.json")

# Se não existir, pede upload
if df is None:
    st.warning("Arquivo `dados.json` não encontrado na pasta do app. Faça upload do arquivo JSON ou coloque `dados.json` na mesma pasta do app.")
    uploaded = st.file_uploader("Enviar dados.json", type=["json"])
    if uploaded:
        df = load_json_from_uploader(uploaded)
    else:
        st.stop()

# -------------------------
# Pré-processamento simples
# -------------------------
# tenta converter colunas numéricas automaticamente
for col in df.columns:
    # remove espaços no começo/fim de nomes
    df.rename(columns={col: col.strip()}, inplace=True)

# tentar converter tipos numéricos quando fizer sentido
for col in df.columns:
    # se mais da metade das células forem convertíveis para número, converte
    non_null = df[col].dropna().astype(str)
    convertible = non_null.apply(lambda x: x.replace(",", ".").replace(" ", "")).str.replace(r'[^\d\.\-]', '', regex=True)
    num_count = convertible.replace('', pd.NA).dropna().shape[0]
    if num_count >= max(1, int(0.5 * max(1, non_null.shape[0]))):
        # tenta conversão segura
        try:
            df[col] = pd.to_numeric(non_null.apply(lambda x: x.replace(",", ".") if isinstance(x, str) else x), errors="coerce")
