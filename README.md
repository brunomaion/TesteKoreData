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

```bash
.\auto.bat
```

### Configuração do Banco de Dados local

Para configurar o banco de dados PostgreSQL e preparar o ambiente para a análise de dados, foi criado um arquivo de configuração SQL (`config.sql`), onde o usuário pode editar as credenciais de acordo com o servidor utilizado.

## Pré-processamento


O código carrega os dados a partir de um arquivo Excel (`Online Retail.xlsx`) para um DataFrame `df`.   
- As colunas de tipo `object` são convertidas para o tipo `string`, padronizando o formato textual dos dados.
- A coluna `InvoiceDate` é transformada para um formato de data.
- Uma coluna `TotalPrice` é criada, calculando o preço total para cada transação como o produto entre `UnitPrice` e `Quantity`.
- A coluna `CustomerID` é convertida para um tipo `string`, após garantir que valores nulos sejam representados corretamente.

O dicionário `stock_dict` armazena uma relação entre códigos de estoque (`StockCode`) e descrições de produtos (`Description`). Caso uma linha não contenha uma descrição, o código busca a última descrição válida para o mesmo código de estoque, garantindo consistência nas descrições.

Um novo DataFrame `dfnew` é criado como uma cópia de `df`. A coluna `Description` é atualizada com base nas informações de `stock_dict`, substituindo valores ausentes com as descrições correspondentes. O DataFrame final é então exportado para um arquivo CSV (`processada.csv`).

## Dashboard Interativa com Streamlit

![alt text](imagens/image.png)

Para facilitar a visualização e análise dos dados, foi desenvolvida uma dashboard interativa utilizando a biblioteca Streamlit. Para executar a dashboard, utilize o comando abaixo no terminal:

```bash
streamlit run dashboard.py
```
Certifique-se de estar no diretório onde o arquivo `dashboard.py` está localizado. A aplicação será aberta em seu navegador padrão, permitindo a interação com os dados.

#### Filtros Disponíveis:
1. **Seleção de Países**: Permite selecionar um ou mais países para filtrar os dados exibidos.
2. **Máximo de registros por Exibição**: Define o número máximo de registros a serem exibidos em cada visualização.

![alt text](imagens/image-1.png)

### Indicadores Utilizados na Dashboard

A dashboard apresenta os seguintes indicadores:

#### Indicadores de Vendas:
1. **Receita Total**: Valor total das vendas realizadas.
2. **Receita Diária/Mensal**: Receita acumulada por dia e por mês.
3. **Receita por País**: Receita gerada por cada país.

#### Indicadores de Clientes:
1. **Clientes Únicos**: Número de clientes distintos.
2. **Top Clientes**: Clientes que mais contribuíram para a receita.
3. **Frequência de Compras por Cliente**: Número médio de compras por cliente.

#### Indicadores de Produtos:
1. **Produtos Mais Vendidos**: Produtos com maior quantidade vendida.
2. **Produtos com Melhor Desempenho por Categoria**: Produtos que geraram maior receita em cada categoria.
3. **Produtos Mais Devolvidos**: Produtos com maior número de devoluções.

#### Indicadores de Transações:
1. **Número de Transações**: Total de transações realizadas.
2. **Transações com Devoluções**: Transações que incluíram devoluções.
3. **Ticket Médio**: Valor médio por transação.

#### Análise Temporal:
1. **Variação Sazonal nas Vendas**: Análise das variações sazonais nas vendas.
2. **Tendência de Vendas ao Longo do Tempo**: Tendência das vendas ao longo do período analisado.

A dashboard foi projetada para ser intuitiva e fácil de usar, permitindo que os usuários filtrem e explorem os dados conforme necessário para obter insights valiosos.

# SQL

Optei por manipular os dados utilizando Python, fazendo apenas uma requisição SQL, devido ao desempenho. No entanto, abaixo estão algumas consultas que foram testadas para verificar a integridade do banco e da análise:

![Banco de Dados](imagens/sql/1-banco.png)

![Relação de Dados](imagens/sql/2-relacaoInvoices.png)

### Consultas SQL

```sql
-- Verificar o número total de transações
SELECT COUNT(*) AS total_transacoes FROM invoices;
```

![alt text](imagens/sql/image.png)

```sql
-- Verificar o número total de clientes
SELECT COUNT(DISTINCT CustomerID) AS total_clientes FROM invoices;
```

![alt text](imagens/sql/image-1.png)

```sql
-- Verificar a receita total
SELECT SUM(UnitPrice * Quantity) AS receita_total FROM invoices;
```

![alt text](imagens/sql/image-2.png)

```sql
-- Verificar a receita por país
SELECT Country, SUM(UnitPrice * Quantity) AS receita_pais FROM invoices GROUP BY Country ORDER BY receita_pais DESC;
```

![alt text](imagens/sql/image-3.png)

```sql
-- Verificar os produtos mais vendidos
SELECT StockCode, Description, SUM(Quantity) AS quantidade_vendida FROM invoices GROUP BY StockCode, Description ORDER BY quantidade_vendida DESC LIMIT 10;
```

![alt text](imagens/sql/image-4.png)

```sql
-- Verificar os clientes que mais contribuíram para a receita
SELECT CustomerID, SUM(UnitPrice * Quantity) AS receita_cliente FROM invoices GROUP BY CustomerID ORDER BY receita_cliente DESC LIMIT 10;
```

![alt text](imagens/sql/image-5.png)



# PowerBI

# Conexão

![alt text](pbi.png)


# DASH

![alt text](imagens/dash/image.png)
![alt text](imagens/dash/image-1.png)
![alt text](imagens/dash/image-2.png)
![alt text](imagens/dash/image-3.png)
![alt text](imagens/dash/image-4.png)
![alt text](imagens/dash/image-5.png)
![alt text](imagens/dash/image-6.png)
![alt text](imagens/dash/image-7.png)