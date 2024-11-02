import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dir = 'planilha/Online Retail.xlsx'
df = pd.read_excel(dir)

table_size = len(df)

df = df.astype({col: 'string' for col in df.select_dtypes(include='object').columns})

df['CustomerID'] = df['CustomerID'].astype('Int64')
df['CustomerID'] = df['CustomerID'].astype('string')


# Dicionário StockCode e Descrição
stock_dict = {}

for index, row in df.iterrows():
    stock_code = row['StockCode']

    if pd.notna(row['Description']):
        stock_dict[stock_code] = row['Description']
    else:
        #None = procura no df
        valid_description = None
        for prev_index in range(index - 1, -1, -1):
            if df.at[prev_index, 'StockCode'] == stock_code and pd.notna(df.at[prev_index, 'Description']):
                valid_description = df.at[prev_index, 'Description']
                break

        if valid_description:
            stock_dict[stock_code] = valid_description
        else:
            stock_dict[stock_code] = "SemDescricao"


dfnew = df.copy()
dfnew['Description'] = dfnew.apply(
    lambda row: stock_dict[row['StockCode']] if pd.isna(row['Description']) else row['Description'], axis=1
)
dfnew.to_csv('planilha/processada.csv', index=False)

print('\n\n PRÉ-PROCESSAMENTO FINALIZADO!\n\n')