import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

st.set_page_config(page_title="Análise de Redes", layout="wide")
st.title("Análise e Visualização da Rede Wikipedia")
st.write("Esta aplicação analisa e visualiza uma rede de conexões extraída da Wikipedia.")

try:
    df = pd.read_csv("network_analysis.csv")

    st.success("Dataset da rede carregado com sucesso!")

    if 'source' in df.columns and 'target' in df.columns:
        G = nx.from_pandas_edgelist(df, 'source', 'target')

        st.header("Informações Básicas da Rede")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Número de Nós (Vértices)", value=G.number_of_nodes())
        with col2:
            st.metric(label="Número de Arestas (Ligações)", value=G.number_of_edges())

        st.header("Visualização Interativa da Rede")
        net = Network(height='700px', width='100%', notebook=True, bgcolor="#222222", font_color="white")
        net.from_nx(G)
        net.show_buttons(filter_=['physics'])

        html_content = net.generate_html()
        st.components.v1.html(html_content, height=720)
    else:
        st.error("Erro no CSV: As colunas 'source' e 'target' são necessárias.")
except FileNotFoundError:
    st.error("ERRO: O arquivo CSV da rede não foi encontrado no repositório. Verifique o nome do arquivo.")
except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")
