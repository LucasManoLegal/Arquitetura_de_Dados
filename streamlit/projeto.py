import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações iniciais
st.set_page_config(page_title="Dashboard de Vendas", page_icon="🛒", layout="wide")

df = pd.read_excel("Vendas.xlsx")

# Filtros
st.sidebar.header("Selecione os Filtros:")

# Filtro 1 - Por Loja
lojas = st.sidebar.multiselect(
    "Lojas",
    options=df["ID Loja"].unique(),
    default=df["ID Loja"].unique(),
    key="loja"
)

# Filtro 2 - Por Produto
produtos = st.sidebar.multiselect(
    "Produtos",
    options=df["Produto"].unique(),
    default=df["Produto"].unique(),
    key="produto"
)

# Filtrar o DataFrame, de acordo com as opções selecionadas
df_selecionado = df.query("`ID Loja` in @lojas and Produto in @produtos")

# Gráficos e na função da página
def Home():
    st.title("Faturamento das lojas💰")

    total_vendas = df["Quantidade"].sum()
    media = df["Quantidade"].mean()
    mediana = df["Quantidade"].median()

    total1, total2, total3 = st.columns(3)
    with total1:
        # Apresentar indicadores rápidos
        st.metric("Total Vendido:", value=int(total_vendas))
    with total2:
        st.metric("Média (Por Produto):", value=f"{media:.1f}")
    with total3:
        st.metric("Mediana (Por Produto):", value=mediana)

    st.markdown("---")

def Graficos():
    # Criar um gráfico de barras, mostrando a quantidade de produtos por loja
    fig_barras = px.bar(
        df_selecionado,
        x="Produto",
        y="Quantidade",
        color="ID Loja",
        barmode="group",
        title="Quantidade de Produtos Vendidos por Loja 🏪")

    # Gráfico de linha, mostrando o total de vendas por loja
    fig_linha = px.line(
        df_selecionado.groupby(["ID Loja"]).sum(numeric_only=True).reset_index(),
        x="ID Loja",
        y="Quantidade", 
        title="Total de Vendas por Loja 💸")

    graf1, graf2 = st.columns(2)

    with graf1:
        st.plotly_chart(fig_barras, use_container_width=True)
    with graf2:
        st.plotly_chart(fig_linha, use_container_width=True)

def SideBar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title="Menu",
            options=["Home", "Gráficos"],
            icons=["house", "bar-chart"],
            default_index=0
        )
    
    if selecionado == "Home":
        Home()
        Graficos()
    else:
        Graficos()

SideBar()