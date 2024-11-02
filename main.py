import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título do dashboard
st.title("Dashboard de Exemplo com Streamlit")

# Descrição
st.write("Este é um exemplo de dashboard criado com o Streamlit para visualização de dados fictícios.")

# Gerando dados fictícios
data = {
    "Categoria": ["A", "B", "C", "D"],
    "Valores": np.random.randint(50, 200, size=4)
}
df = pd.DataFrame(data)

# Exibindo o DataFrame
st.subheader("Dados")
st.dataframe(df)

# Gráfico de barras
st.subheader("Gráfico de Barras")
fig, ax = plt.subplots()
ax.bar(df["Categoria"], df["Valores"], color="skyblue")
ax.set_xlabel("Categoria")
ax.set_ylabel("Valores")
ax.set_title("Valores por Categoria")
st.pyplot(fig)

# Slider de intervalo para visualização personalizada
st.subheader("Visualização de Intervalo")
valor_min = st.slider("Valor Mínimo", min_value=int(df["Valores"].min()), max_value=int(df["Valores"].max()), value=int(df["Valores"].min()))
valor_max = st.slider("Valor Máximo", min_value=int(df["Valores"].min()), max_value=int(df["Valores"].max()), value=int(df["Valores"].max()))
df_filtered = df[(df["Valores"] >= valor_min) & (df["Valores"] <= valor_max)]

# Exibindo o DataFrame filtrado
st.write("Dados filtrados:")
st.dataframe(df_filtered)
