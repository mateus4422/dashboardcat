import streamlit as st
import pandas as pd

# Exibir o logotipo centralizado com tamanho 200x200
st.image("farma.png", use_column_width=False, caption="", output_format="PNG", width=200)

# Carregar os dados do Excel
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSulTerCVzXwOlraQucdzZsvxg-XGDZPA9xAXiMpFkQJ7GlfisoPoWzh3MrJEKCQPZYnDer7Cd0u5qE/pubhtml"
df = pd.read_excel(url, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Lê todas as colunas

# Renomear as colunas
df.columns = ["Razão Social", "Período Inicial", "Período Final", "Loja", "CNPJ", "Faturamento ST", "Ressarcimento", "Complemento", "% Ressarcimento", "Status", "Prioridade"]

# Função para formatar o valor em "R$ 75.809.091,57"
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(".", ",")

# Widget de seleção de Razão Social
razao_social_opcoes = ["Selecionar todos"] + list(df["Razão Social"].unique())
razao_social_selecionada = st.selectbox("Selecione a Razão Social:", razao_social_opcoes)

# Filtrar dados pela Razão Social selecionada
if razao_social_selecionada == "Selecionar todos":
    dados_razao_social_selecionada = df
else:
    dados_razao_social_selecionada = df[df["Razão Social"] == razao_social_selecionada]

# Widget de seleção de status
status_selecionado = st.selectbox("Selecione o Status:", dados_razao_social_selecionada["Status"].unique())

# Filtrar dados pelo status selecionado
dados_status_selecionado = dados_razao_social_selecionada[dados_razao_social_selecionada["Status"] == status_selecionado]

# Adicionar menu lateral para escolher entre "Prioridade" e "Geral"
menu_selecionado = st.sidebar.radio("Selecione o Menu:", ["Prioridade", "Geral"])

# Filtro de Lojas
if menu_selecionado == "Prioridade":
    lojas = dados_status_selecionado[dados_status_selecionado["Prioridade"] == "Sim"]["Loja"].unique()
else:
    lojas = dados_status_selecionado["Loja"].unique()

lojas_selecionadas = st.multiselect("Selecione as lojas:", ["Selecionar todos"] + lojas.tolist(), default="Selecionar todos", key="lojas", help="Escolha uma ou mais lojas")

# Filtrar dados das lojas selecionadas
if "Selecionar todos" not in lojas_selecionadas:
    dados_lojas_selecionadas = dados_status_selecionado[dados_status_selecionado["Loja"].isin(lojas_selecionadas)]
else:
    dados_lojas_selecionadas = dados_status_selecionado

# Organizar os blocos de total em uma grade
total_container = st.container()
total_block = st.columns(5)

# Estilo para centralizar e formatar os valores
value_style = "display: flex; justify-content: center; align-items: center; text-align: center; border: 2px solid #FF6400; padding: 10px; font-size: 20px;"

# Bloco de Faturamento ST
with total_block[0]:
    st.subheader("Faturamento ST")
    total_faturamento_st = dados_lojas_selecionadas["Faturamento ST"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_faturamento_st)}</div>', unsafe_allow_html=True)

# Bloco de Ressarcimento
with total_block[1]:
    st.subheader("Ressarcimento")
    total_ressarcimento = dados_lojas_selecionadas["Ressarcimento"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_ressarcimento)}</div>', unsafe_allow_html=True)

# Bloco de Complemento
with total_block[2]:
    st.subheader("Complemento")
    total_complemento = dados_lojas_selecionadas["Complemento"].sum()
    st.markdown(f'<div style="{value_style}">{formatar_valor(total_complemento)}</div>', unsafe_allow_html=True)

# Bloco de Diferença Ressarcimento - Complemento
with total_block[3]:
    st.subheader("Ressar - Compl")
    diferenca_ressarcimento_complemento = total_ressarcimento - total_complemento
    st.markdown(f'<div style="{value_style}">{formatar_valor(diferenca_ressarcimento_complemento)}</div>', unsafe_allow_html=True)

# Calculadora de Média % Ressarcimento apenas para "Em Desenvolvimento"
if status_selecionado == "Em Desenvolvimento":
    with total_block[4]:
        st.subheader("% Ressarcimento")
        
        if not dados_lojas_selecionadas.empty:
            media_percentual_ressarcimento = dados_lojas_selecionadas["% Ressarcimento"].mean() * 100
            st.markdown(f'<div style="{value_style}">{media_percentual_ressarcimento:.1f}%</div>', unsafe_allow_html=True)

            # Widget de entrada para a porcentagem
            nova_porcentagem = st.number_input("Nova Porcentagem (%)", min_value=0.0, max_value=100.0, value=media_percentual_ressarcimento)
            
            # Calcular o novo valor de ressarcimento com base na nova porcentagem
            novo_ressarcimento = total_faturamento_st * (nova_porcentagem / 100)
            st.markdown(f'<div style="{value_style}">Novo Ressarcimento: {formatar_valor(novo_ressarcimento)}</div>', unsafe_allow_html=True)
        else:
            st.write("Apenas nos Status 'Em Desenvolvimento'")
else:
    with total_block[4]:
        st.subheader("%Ressarcimento")
        st.write("Apenas nos outros Status")

# Gráfico de Barras (Faturamento ST)
st.subheader("Gráfico de Barras (Faturamento ST)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Faturamento ST"], use_container_width=True)

# Gráfico de Barras (Ressarcimento)
st.subheader("Gráfico de Barras (Ressarcimento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Ressarcimento"], use_container_width=True)

# Gráfico de Barras (Complemento)
st.subheader("Gráfico de Barras (Complemento)")
st.bar_chart(dados_lojas_selecionadas.set_index("Loja")["Complemento"], use_container_width=True)
