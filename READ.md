# Analise de dados para vaga de estágio KoreData

## Introdução

Para esta análise de dados, utilizei a base de dados disponível no link [Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail). Esta base contém transações de uma loja online do Reino Unido, registradas entre 01/12/2010 e 09/12/2011.

### Instalação e preparação do ambiente

Para realizar a análise de dados, é necessário instalar algumas bibliotecas adicionais. Execute os seguintes comandos para instalar o PostgreSQL, psycopg2, pandas, Streamlit, Matplotlib e NumPy:

```bash

# Instale o PostgreSQL
sudo apt-get install postgresql postgresql-client

# Instale o psycopg2
pip install psycopg2-binary

# Instale o pandas
pip install pandas

# Instale o Streamlit
pip install streamlit

# Instale o Matplotlib
pip install matplotlib

# Instale o NumPy
pip install numpy
```

## Automatização

Para automatizar o processo de pré-processamento dos dados, criação do banco de dados `online_retail`, da tabela `invoices` e inserção dos dados processados no banco, foram criados dois scripts: um para Linux (`auto.sh`) e outro para Windows (`auto.bat`). Esses scripts realizam as etapas necessárias para preparar o ambiente e carregar os dados no banco de dados.
Para executar, basta abrir o terminal no diretório principal e executtar o comando abaixo:

'''bash
.\auto.bat
'''

## Pré processamento



## Análise de dados
a. Indicadores de Vendas:
  1. Receita Total
  2. Receita Diária/Mensal
  3. Receita por País

b. Indicadores de Clientes:
  1. Clientes Únicos
  2. Top Clientes
  3. Frequência de Compras por Cliente

c. Indicadores de Produtos:
  1. Produtos Mais Vendidos
  2. Produtos com Melhor Desempenho por Categoria
  3. Produtos Mais Devolvidos

d. Indicadores de Transações:
  1. Número de Transações
  2. Transações com Devoluções
  3. Ticket Médio

e. Análise Temporal:
  1. Variação Sazonal nas Vendas
  2. Tendência de Vendas ao Longo do Tempo


### ANOTAÇOES

Descontos e devoluções não foram possiveis ser contabilizadas devido a não possuirem preço de devolução, o que pode ser realizado é um tratamento de busca no pré processamen
Consultas diretas no SQL com a dah tem um
tempo de espera muito grande