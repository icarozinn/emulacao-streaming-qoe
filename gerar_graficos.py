#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('resultados_streaming.csv')

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11})

# --- GRÁFICO 1: STARTUP DELAY CON IC ---
plt.figure(figsize=(10, 6))
sns.barplot(
    data=df[df['Protocolo'] == 'MPEG-DASH'], 
    x='Condicao_Rede', 
    y='Startup_Delay_S', 
    hue='Chunk_Size_S',
    palette='Blues_d',
    errorbar=('ci', 95) # <- Adiciona a barra de erro do Intervalo de Confiança!
)
plt.title('Startup Delay Médio com Intervalo de Confiança (95%)')
plt.xlabel('Condição da Rede WAN')
plt.ylabel('Tempo até o Play (Segundos)')
plt.legend(title='Tamanho do Chunk (s)')
plt.tight_layout()
plt.savefig('grafico_startup_delay.png', dpi=300)

# --- GRÁFICO 2: STALL RATIO CON IC ---
plt.figure(figsize=(10, 6))
df_oscilante = df[df['Condicao_Rede'] == 'Oscilante']
sns.barplot(
    data=df_oscilante, 
    x='Protocolo', 
    y='Stall_Ratio_Pct', 
    hue='Chunk_Size_S',
    palette='Oranges_d',
    errorbar=('ci', 95) # <- Adiciona a barra de erro do Intervalo de Confiança!
)
plt.title('Taxa de Travamento (Stall Ratio) na Instabilidade com IC (95%)')
plt.xlabel('Protocolo de Streaming')
plt.ylabel('Tempo Travado em Buffering (%)')
plt.ylim(0, 110)
plt.legend(title='Tamanho do Chunk (s)')
plt.tight_layout()
plt.savefig('grafico_stall_ratio.png', dpi=300)

print("📊 Gráficos científicos com Intervalo de Confiança gerados!")
