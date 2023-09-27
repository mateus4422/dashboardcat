import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados do Excel online
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=csv"
df = pd.read_csv(url)

# Define a função para determinar o período (P1 ou P2) com base na data
def determinar_periodo(data):
    if "01/09/2019" <= data <= "31/10/2020":
        return "P2"
    elif "01/05/2018" <= data <= "30/09/2019":
        return "P1"
    else:
        return ""

# Adiciona a coluna "Período" com base na data
df["Período"] = df["Periodo Inicial"].apply(determinar_periodo)

# Título do dashboard
st.title("Dashboard de Análise de Lojas")

# Filtro de Lojas (CheckBox)
lojas = st.multiselect("Selecione as Lojas:", df["Loja"].unique())

# Filtro Geral
filtro_geral = st.checkbox("Filtro Geral")

# Filtra os dados com base nas lojas selecionadas e no filtro geral
if filtro_geral:
    df_filtrado = df if not lojas else df[df["Loja"].isin(lojas)]
else:
    df_filtrado = df[df["Loja"].isin(lojas)]

# Exibe as informações das lojas selecionadas
for loja in df_filtrado["Loja"].unique():
    st.subheader(f"Loja: {loja}")
    
    # Dados em números
    st.write("Faturamento ST:", df_filtrado[df_filtrado["Loja"] == loja]["Faturamento ST"].sum())
    st.write("Ressarcimento:", df_filtrado[df_filtrado["Loja"] == loja]["Ressarcimento"].sum())
    
    # Converte a coluna "% Ressarcimento" para valores numéricos
    percent_r = df_filtrado[df_filtrado["Loja"] == loja]["% Ressarcimento"].str.replace(',', '.').str.rstrip('%').astype(float)
    st.write("% Ressarcimento:", percent_r.mean())
    
    st.write("Status:", df_filtrado[df_filtrado["Loja"] == loja]["Status"].iloc[0])

# Gráficos de comparação entre P1 e P2
fig, ax = plt.subplots(3, 1, figsize=(8, 12))
for i, col in enumerate(["Faturamento ST", "Ressarcimento", "% Ressarcimento"]):
    df_p1 = df_filtrado[df_filtrado["Período"] == "P1"]
    df_p2 = df_filtrado[df_filtrado["Período"] == "P2"]
    
    # Converte os valores para inteiros
    p1_value = int(df_p1[col].sum())
    p2_value = int(df_p2[col].sum())
    
    ax[i].bar(["P1", "P2"], [p1_value, p2_value])
    ax[i].set_ylabel(col)
    ax[i].set_title(f"Comparação entre P1 e P2 - {col}")

st.pyplot(fig)


# Resumo geral
if filtro_geral:
    st.subheader("Resumo Geral")
    
    # Dados em números
    st.write("Faturamento ST (Total):", df_filtrado["Faturamento ST"].sum())
    st.write("Ressarcimento (Total):", df_filtrado["Ressarcimento"].sum())
    
    # Converte a coluna "% Ressarcimento" para valores numéricos
    percent_r_total = df_filtrado["% Ressarcimento"].str.replace(',', '.').str.rstrip('%').astype(float)
    st.write("% Ressarcimento (Total):", percent_r_total.mean())
    
    # Gráficos de comparação das lojas
    fig2, ax2 = plt.subplots(2, 1, figsize=(8, 8))
    for i, col in enumerate(["Faturamento ST", "Ressarcimento"]):
        ax2[i].bar(df_filtrado["Loja"], df_filtrado[col])
        ax2[i].set_ylabel(col)
        ax2[i].set_title(f"Comparação entre Lojas - {col}")
        ax2[i].tick_params(axis="x", rotation=45)
    st.pyplot(fig2)
