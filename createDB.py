import psycopg2
from psycopg2 import sql
import pandas as pd

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

# Lê as configurações do arquivo
arquivo_config = 'configSQL.txt'
configuracoes = ler_config(arquivo_config)

host = configuracoes.get('host')
port = configuracoes.get('port')
user = configuracoes.get('user')
password = configuracoes.get('password')
nome_banco = configuracoes.get('nome_banco')

print(f"Host: {host}")
print(f"Porta: {port}")
print(f"Usuário: {user}")
print(f"Senha: {password}")
print(f"Nome do Banco: {nome_banco}")

# Variáveis para conexão e cursor
conn = None
cursor = None

# Conexão inicial para criar o banco de dados
try:
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.autocommit = True 
    cursor = conn.cursor()
    
    # Criação do banco de dados
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(nome_banco)))
    print(f"Banco de dados '{nome_banco}' criado com sucesso!")

except Exception as e:
    print(f"Erro ao criar o banco de dados: {e}")

# Tente conectar ao banco de dados
try:
    conn = psycopg2.connect(dbname=nome_banco, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    #print("Conexão ao banco de dados estabelecida com sucesso!")

    # Criação da tabela
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS invoices (
        InvoiceNo VARCHAR(255) NOT NULL,
        StockCode VARCHAR(255) NOT NULL,
        Description TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        InvoiceDate TIMESTAMP NOT NULL,
        UnitPrice NUMERIC(10, 2) NOT NULL,
        CustomerID VARCHAR(255),
        Country VARCHAR(255) NOT NULL,
        TotalPrice NUMERIC(10, 2) NOT NULL
    );
    """)
    conn.commit()  # Commit da transação
    print("Tabela 'invoices' criada com sucesso!")

except Exception as e:
    print(f"Erro ao conectar ao banco de dados ou criar a tabela: {str(e)}")

try:
    # Ler o arquivo CSV
    df = pd.read_csv('planilha/processada.csv')
    conn = psycopg2.connect(dbname=nome_banco, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    # Inserir os dados do DataFrame na tabela "invoices"
    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO invoices (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country, TotalPrice)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, row)

    conn.commit()  # Confirma as alterações no banco de dados
    print("Dados inseridos com sucesso!")

    # Fecha a conexão e o cursor
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Erro ao inserir dados na tabela: {e}")

finally:
    # Fecha a conexão e o cursor, se abertos
    if cursor:
        cursor.close()
    if conn:
        conn.close()