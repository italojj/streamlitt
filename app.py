import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

st.set_page_config(page_title="Análise de Redes", layout="wide")
st.title("Ferramenta para Análise e Visualização de Redes")

st.write("Faça o upload de um arquivo CSV com as colunas 'source' e 'target' para visualizar a rede.")

uploaded_file = st.file_uploader(
    "Selecione seu arquivo CSV",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if 'source' in df.columns and 'target' in df.columns:
            G = nx.from_pandas_edgelist(df, 'source', 'target')

            st.header("Informações Básicas da Rede")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Número de Nós (Vértices)", value=G.number_of_nodes())
            with col2:
                st.metric(label="Número de Arestas (Ligações)", value=G.number_of_edges())

            st.header("Visualização Interativa da Rede")
            net = Network(height='600px', width='100%', notebook=True, bgcolor="#222222", font_color="white")
            net.from_nx(G)
            net.show_buttons(filter_=['physics'])

            html_content = net.generate_html()
            st.components.v1.html(html_content, height=620)
        else:
            st.error("Erro: O arquivo CSV precisa ter as colunas 'source' e 'target'.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    st.info("Aguardando o upload de um arquivo CSV.")
