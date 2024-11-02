import psycopg2
from psycopg2 import sql

def ler_config(arquivo):
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

finally:
    # Fecha a conexão e o cursor
    if cursor:
        cursor.close()
    if conn:
        conn.close()
