import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pub?output=xlsx"
df = pd.read_excel(url, usecols=[1, 2, 3, 4, 5, 6, 7, 8], skiprows=0)  # Começa da primeira linha (skiprows=0)

# Renomear as colunas
df.columns = ["Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "% Ressarcimento", "Status"]

# Formatar as colunas de data para exibir apenas mês e ano
df["Período Inicial"] = pd.to_datetime(df["Período Inicial"]).dt.strftime('%b %Y')
df["Período Final"] = pd.to_datetime(df["Período Final"]).dt.strftime('%b %Y')

# Adicionar coluna de P1 ou P2 com base nas datas
df["P1_P2"] = "P1"  # Inicialmente, todas as linhas são definidas como P1
df.loc[df["Período Inicial"] >= "Sep 2019", "P1_P2"] = "P2"  # Definir como P2 se a data inicial for posterior a Sep 2019

# Calcular a média de ressarcimento da seguinte maneira: (Ressarcimeento - 100) / Faturamento
df["Media Ressarcimento"] = ((df["Ressarcimento"] - 100) / df["Faturamento ST"]) * 100

# Filtro de Lojas (checkboxes)
lojas = df["Loja"].unique()
lojas_selecionadas = st.multiselect("Selecione as lojas para comparação:", lojas, default=lojas)

# Exibir o logotipo

st.image("farma.png", use_column_width=True)  # Nome da imagem do logotipo


# Resumo Geral
st.write("Resumo Geral:")

# Bloco de Total Faturamento ST
st.subheader("Total Faturamento ST")
total_faturamento_st = df["Faturamento ST"].sum()
st.write(f"R$ {total_faturamento_st:,.2f}")

# Bloco de Total Ressarcimento
st.subheader("Total Ressarcimento")
total_ressarcimento = df["Ressarcimento"].sum()
st.write(f"R$ {total_ressarcimento:,.2f}")

# Bloco de Média % Ressarcimento
st.subheader("Média % Ressarcimento")
media_percentual_ressarcimento = df["% Ressarcimento"].mean()
st.write(f"{media_percentual_ressarcimento:.2f}%")

# Gráfico de Barras (Faturamento ST e Ressarcimento)
st.subheader("Comparação Faturamento ST e Ressarcimento por Loja")
fig = px.bar(
    df[df["Loja"].isin(lojas_selecionadas)],
    x="Loja",
    y=["Faturamento ST", "Ressarcimento"],
    title="Comparação Faturamento ST e Ressarcimento por Loja",
    labels={"value": "Valor (R$)"},
)
fig.update_layout(
    legend_title_text="Loja",
    xaxis_title="",
    yaxis_title="Valor (R$)",
    xaxis={'categoryorder': 'total descending'}
)
st.plotly_chart(fig)

# Exibir informações detalhadas das lojas selecionadas
st.subheader("Informações Detalhadas das Lojas Selecionadas")
if not lojas_selecionadas:
    st.write("Selecione uma ou mais lojas para ver informações detalhadas.")
else:
    for loja in lojas_selecionadas:
        st.subheader(loja)
        dados_loja = df[df["Loja"] == loja]
        st.write(dados_loja)

# Gráfico de Barras (Média % Ressarcimento por Loja)
st.subheader("Média % Ressarcimento por Loja")
fig2 = px.bar(
    df[df["Loja"].isin(lojas_selecionadas)],
    x="Loja",
    y="Media Ressarcimento",
    title="Média % Ressarcimento por Loja",
    labels={"Media Ressarcimento": "Média % Ressarcimento"},
)
fig2.update_layout(
    xaxis_title="",
    yaxis_title="Média % Ressarcimento",
    xaxis={'categoryorder': 'total descending'}
)
st.plotly_chart(fig2)
