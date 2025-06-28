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
        minimum_degree = 3
        nodes_selected = [n for n, d in G.degree() if d > minimum_degree]
        G_subsubgraph = G.subgraph(nodes_selected)
        st.info(f"Rede original: {G.number_of_nodes()} nós. | Exibindo rede reduzida (nós com mais de {minimum_degree} conexões): {G_subsubgraph.number_of_nodes()} nós.")
        st.header("Informações Básicas da Rede")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Número de Nós (Vértices)", value=G_subsubgraph.number_of_nodes())
        with col2:
            st.metric(label="Número de Arestas (Ligações)", value=Gsubsubgraph.number_of_edges())

        st.header("Visualização Interativa da Rede")
        net = Network(height='700px', width='100%', notebook=True, bgcolor="#222222", font_color="white")
        net.from_nx(G_subsubgraph)
        net.show_buttons(filter_=['physics'])

        html_content = net.generate_html()
        st.components.v1.html(html_content, height=720)
    else:
        st.error("Erro no CSV: As colunas 'source' e 'target' são necessárias.")
except FileNotFoundError:
    st.error("ERRO: O arquivo CSV da rede não foi encontrado no repositório. Verifique o nome do arquivo.")
except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")
