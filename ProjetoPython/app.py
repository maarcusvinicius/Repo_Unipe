import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Análise USD/BRL", page_icon="📈", layout="wide")

st.title("Análise da Cotação do Dólar (USD/BRL)")
st.markdown("""
Visualização interativa da cotação histórica do dólar frente ao real.
""")

@st.cache_data 
def load_data():
    df = pd.read_csv('USD_BRL_hist.csv')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
    df = df.sort_values('Data')
    df['Ano'] = df['Data'].dt.year
    df = df.rename(columns={'USD_BRL': 'Close'})
    return df

df = load_data()

st.sidebar.header("Filtros")
selected_years = st.sidebar.multiselect(
    "Selecione os anos:",
    options=sorted(df['Ano'].unique()),
    default=sorted(df['Ano'].unique())
)

filtered_df = df[df['Ano'].isin(selected_years)]

st.subheader("📊 Métricas Principais")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Período Analisado", f"{filtered_df['Data'].min().year} - {filtered_df['Data'].max().year}")
with col2:
    st.metric("Cotação Média", f"R$ {filtered_df['Close'].mean():.2f}")
with col3:
    st.metric("Maior Valor", f"R$ {filtered_df['Close'].max():.2f}")

# Gráfico 1: Série Temporal
st.subheader("📈 Cotação ao Longo do Tempo")
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(filtered_df['Data'], filtered_df['Close'], color='blue')
ax1.set_title("Cotação de Fechamento do Dólar (USD/BRL)")
ax1.set_xlabel("Data")
ax1.set_ylabel("Valor em R$")
ax1.grid(True)
st.pyplot(fig1)

# Gráfico 2: Histograma
st.subheader("📊 Distribuição das Cotações")
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.hist(filtered_df['Close'], bins=30, color='skyblue', edgecolor='black')
ax2.set_title("Distribuição dos Valores de Fechamento")
ax2.set_xlabel("Valor em R$")
ax2.set_ylabel("Frequência")
ax2.grid(True)
st.pyplot(fig2)

# Gráfico 3: Boxplot por Ano
st.subheader("📦 Variação Anual (Boxplot)")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.boxplot(
    x='Ano', 
    y='Close', 
    data=filtered_df, 
    hue='Ano', 
    palette='coolwarm', 
    legend=False,
    ax=ax3
)
ax3.set_title("Variação Anual da Cotação")
ax3.set_xlabel("Ano")
ax3.set_ylabel("Valor em R$")
ax3.grid(True)
st.pyplot(fig3)