import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

st.title("Online Retail")

def ler_config(arquivo):
    """Lê as configurações de conexão a partir de um arquivo."""
    config = {}
    with open(arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                chave, valor = linha.split('=', 1) 
                config[chave.strip()] = valor.strip().strip('"')  
    return config


arquivo_config = 'configSQL.txt'
configuracoes = ler_config(arquivo_config)

host = configuracoes.get('host')
port = configuracoes.get('port')
user = configuracoes.get('user')
password = configuracoes.get('password')
dbname = configuracoes.get('nome_banco')

#conexão com o banco de dados
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname
    )
    st.success("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}")
    conn = None

query = "SELECT * FROM invoices;"
df = pd.read_sql_query(query, conn)

df['customerid'].astype(str)
df['invoicedate'] = pd.to_datetime(df['invoicedate']).dt.date

#FILTROS #########################

st.sidebar.header('Filtros')
st.sidebar.subheader('Países')
unique_countries = df['country'].unique()
selected_countries = st.sidebar.multiselect('Selecione os países', unique_countries)


st.sidebar.subheader("Dataframe")
max_registro = st.sidebar.slider("Registros Máximos", 0, 100, 10)


if selected_countries:
  df = df[df['country'].isin(selected_countries)]

###########################################################################

st.subheader(f'{len(df)} registros')
st.dataframe(df, hide_index=True)

# Exibe o DataFrame agrupado

# Converte a coluna de data para datetime
df['invoicedate'] = pd.to_datetime(df['invoicedate'])







# Receita Total ########################################################################
st.header("Receita")

receita_total = df['totalprice'].sum()
st.metric(label="Total", value=f"R$ {receita_total:.2f}")

# Indicador: Receita Diária/Mensal

df['date'] = pd.to_datetime(df['invoicedate']).dt.date
receita_diaria = df.groupby('date')['totalprice'].sum()



receita_mensal = df.groupby(pd.to_datetime(df['invoicedate']).dt.to_period('M'))['totalprice'].sum()

st.subheader("Receita Diária")


plt.figure(figsize=(10, 5))
plt.plot(receita_diaria.index, receita_diaria.values)
plt.xticks(receita_diaria.index[::30], rotation=45) 
plt.grid(True)
st.pyplot(plt)
st.line_chart(receita_diaria)

# Receita Mensal
st.subheader("Receita Mensal")
receita_mensal.index = receita_mensal.index.to_timestamp()
plt.figure(figsize=(10, 5))
plt.plot(receita_mensal.index, receita_mensal.values, marker='o')
plt.xticks(receita_mensal.index, rotation=45)  
plt.grid(True)
st.pyplot(plt)

st.bar_chart(receita_mensal)

# Receita por país
st.subheader("Receita por País")
grouped_df = df.groupby('country')['totalprice'].sum()
top_paises = grouped_df.sort_values(ascending=False)
top_paises.reset_index()
st.dataframe(top_paises.head(max_registro))
st.bar_chart(top_paises.head(max_registro))



### CLIENTES ########################################################################
st.header('Clientes')

# Indicador: Clientes Únicos
clientes_unicos = df['customerid'].nunique()
st.metric(label="Clientes Únicos", value=clientes_unicos)

# Indicador: Top Clientes
st.write("Top Clientes por Receita:")
top_clientes = df.groupby('customerid')['totalprice'].sum().sort_values(ascending=False).head(10)
st.dataframe(top_clientes.head(max_registro))

# Indicador: Frequência de Compras por Cliente
frequencia_compras = df['customerid'].value_counts()
st.write("Frequência de Compras por Cliente:")
st.dataframe(frequencia_compras.head(max_registro))



### PRODUTOS ########################################################################
st.header("Produtos")

# Indicador: Produtos Mais Vendidos
produtos_mais_vendidos = df.groupby('description')['quantity'].sum().sort_values(ascending=False).head(10)
st.write("Produtos Mais Vendidos:")
st.dataframe(produtos_mais_vendidos.head(max_registro))

# Indicador: Produtos com Melhor Desempenho por Categoria (assumindo que 'StockCode' é a categoria)
melhor_desempenho_categoria = df.groupby('stockcode')['totalprice'].sum().sort_values(ascending=False).head(10)
st.write("Produtos com Melhor Desempenho por Categoria:")
st.dataframe(melhor_desempenho_categoria.head(max_registro))

# Indicador: Produtos Mais Devolvidos
produtos_devolvidos = df[df['quantity'] < 0].groupby('description')['quantity'].sum().sort_values().head(10)
st.write("Produtos Mais Devolvidos:")
st.dataframe(produtos_devolvidos.head(max_registro))




#### TRANSAÇÕES ########################################################################


st.header('Transações')

# Indicador: Número de Transações
num_transacoes = df['invoiceno'].nunique()
st.metric(label="Número de Transações", value=num_transacoes)

# Indicador: Transações com Devoluções
transacoes_devolucao = df[df['quantity'] < 0]['invoiceno'].nunique()
st.metric(label="Transações com Devoluções", value=transacoes_devolucao)

# Indicador: Ticket Médio
ticket_medio = receita_total / num_transacoes
st.metric(label="Ticket Médio", value=f"R$ {ticket_medio:.2f}")