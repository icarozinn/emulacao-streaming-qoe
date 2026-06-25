import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Configuração de tema e fontes para alta legibilidade na apresentação
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 13,
    'legend.title_fontsize': 14
})

# Lendo o arquivo correto com os dados das 30 rodadas
df = pd.read_csv('resultados_streaming.csv')
df_oscilante = df[df['Condicao_Rede'] == 'Oscilante']

# Definição de cores com excelente contraste (Azul Acinzentado vs Azul Escuro)
cores_chunk = ["#94a3b8", "#1e293b"]

# --- GRÁFICO 1: RESOLUÇÃO MÉDIA ---
fig, ax = plt.subplots(figsize=(9, 6), dpi=200)
sns.barplot(
    data=df_oscilante, 
    x="Protocolo", 
    y="Resolucao_Media_P", 
    hue="Chunk_Size_S", 
    palette=cores_chunk,
    errorbar=('ci', 95), # Barras de erro baseadas no intervalo de confiança das 30 rodadas
    capsize=0.05,        # Linha horizontal de acabamento no topo do erro
    ax=ax
)
ax.set_title("Resolução Vertical Média na Instabilidade da Rede (IC 95%)", pad=20, fontweight='bold')
ax.set_xlabel("Protocolo de Streaming", labelpad=10)
ax.set_ylabel("Resolução Vertical (p)", labelpad=10)
ax.set_ylim(0, 1200)
ax.legend(title="Tamanho do Chunk (s)", loc="upper right")
plt.tight_layout()
plt.savefig('grafico_resolucao_media_novo.png')
plt.close()

# --- GRÁFICO 2: STALL RATIO (TAXA DE TRAVAMENTO) ---
fig, ax = plt.subplots(figsize=(9, 6), dpi=200)
sns.barplot(
    data=df_oscilante, 
    x="Protocolo", 
    y="Stall_Ratio_Pct", 
    hue="Chunk_Size_S", 
    palette=["#f0a57a", "#1e293b"], # Laranja suave para destacar visualmente o buffering
    errorbar=('ci', 95),
    capsize=0.05,
    ax=ax
)
ax.set_title("Taxa de Travamento (Stall Ratio) na Instabilidade (IC 95%)", pad=20, fontweight='bold')
ax.set_xlabel("Protocolo de Streaming", labelpad=10)
ax.set_ylabel("Tempo Travado em Buffering (%)", labelpad=10)
ax.set_ylim(0, 100) # Teto natural de 100% para porcentagem
ax.legend(title="Tamanho do Chunk (s)", loc="upper right")
plt.tight_layout()
plt.savefig('grafico_stall_ratio_novo.png')
plt.close()

# --- GRÁFICO 3: STARTUP DELAY ---
fig, ax = plt.subplots(figsize=(9, 6), dpi=200)
sns.barplot(
    data=df, 
    x="Condicao_Rede", 
    y="Startup_Delay_S", 
    hue="Chunk_Size_S", 
    palette=["#38bdf8", "#1e293b"], # Azul vivo para diferenciar bem o cenário
    errorbar=('ci', 95),
    capsize=0.05,
    ax=ax
)
ax.set_title("Atraso de Inicialização (Startup Delay) Médio (IC 95%)", pad=20, fontweight='bold')
ax.set_xlabel("Condição da Rede WAN", labelpad=10)
ax.set_ylabel("Tempo até o Play (Segundos)", labelpad=10)
ax.set_ylim(0, 5.0) # Margem ideal para acomodar a maior barra sem espremer o título
ax.legend(title="Tamanho do Chunk (s)", loc="upper left")
plt.tight_layout()
plt.savefig('grafico_startup_delay_novo.png')
plt.close()

print("[SUCESSO] Novos gráficos limpos e legíveis gerados a partir de resultados_streaming.csv!")
