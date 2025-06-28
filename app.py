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

        st.sidebar.header("Opções de Visualização")
        st.sidebar.write("Escolha como deseja visualizar a rede.")

        tipo_filtro = st.sidebar.selectbox(
            "Selecione um subconjunto do grafo para exibir:",
            ("Rede Completa", 
             "Filtrar por Grau (Nós Mais Conectados)", 
             "Focar no Maior Componente Conectado")
        )

        G_para_exibir = G

        if tipo_filtro == "Filtrar por Grau (Nós Mais Conectados)":
            grau_minimo = st.sidebar.slider(
                "Exibir apenas nós com grau maior que:",
                min_value=0, max_value=100, value=10, step=1
            )
            nos_selecionados = [n for n, d in G.degree() if d > grau_minimo]
            G_para_exibir = G.subgraph(nos_selecionados)
            st.info(f"Exibindo nós com mais de {grau_minimo} conexões.")

        elif tipo_filtro == "Focar no Maior Componente Conectado":
            componentes = nx.connected_components(G)
            maior_componente = max(componentes, key=len)
            G_para_exibir = G.subgraph(maior_componente)
            st.info("Exibindo o maior componente conectado da rede.")
        
        else:
             st.info("Exibindo a rede completa. Pode ser lento para carregar.")


        st.header(f"Informações Básicas da Rede: {tipo_filtro}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Número de Nós (Vértices)", value=G_para_exibir.number_of_nodes())
        with col2:
            st.metric(label="Número de Arestas (Ligações)", value=G_para_exibir.number_of_edges())

        st.header(f"Visualização Interativa: {tipo_filtro}")
        net = Network(height='700px', width='100%', notebook=True, bgcolor="#222222", font_color="white")
        
        with st.spinner("A gerar a visualização... Por favor, aguarde."):
            net.from_nx(G_para_exibir)
            net.show_buttons(filter_=['physics'])
            html_content = net.generate_html()
            st.components.v1.html(html_content, height=720)
    else:
        st.error("Erro no CSV: As colunas 'source' e 'target' são necessárias.")
except FileNotFoundError:
    st.error("ERRO: O ficheiro CSV da rede não foi encontrado no repositório. Verifique o nome do ficheiro.")
except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")
