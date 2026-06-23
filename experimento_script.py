#!/usr/bin/env python3
import time
import csv
import math
import random

# ==============================================================================
# CONFIGURAÇÕES E PARÂMETROS
# ==============================================================================
PROTOCOLOS = ["MPEG-DASH", "Apple-HLS"]
CHUNK_SIZES = [2, 6]
CONDICOES_WAN = {
    "Estavel": {"banda_bps": 10_000_000, "perda_pct": 0, "delay_ms": 10},
    "Oscilante": {"banda_bps": 2_000_000, "perda_pct": 2, "delay_ms": 80}
}

DURACAO_VIDEO_S = 60
RESOLUCAO_BASE = 1080
REPETICOES = 10  # Número de repetições para o Intervalo de Confiança

def simular_player_qoe(protocolo, chunk_size, condicao_nome, rede_config):
    # Puxa as configurações base da rede
    banda = rede_config["banda_bps"]
    perda = rede_config["perda_pct"]
    delay = rede_config["delay_ms"] / 1000.0
    
    # Injeta pequenas variações aleatórias por rodada (simulando instabilidade real)
    if condicao_nome == "Oscilante":
        banda *= random.uniform(0.85, 1.15)
        perda = max(0, perda + random.uniform(-0.5, 0.5))
        delay += random.uniform(-0.01, 0.01)

    total_chunks = math.ceil(DURACAO_VIDEO_S / chunk_size)
    
    # Cálculo do Startup Delay com ruído estocástico
    tamanho_manifesto_bits = 50_000
    tamanho_chunk_base_bits = chunk_size * 4_000_000
    tempo_manifesto = (tamanho_manifesto_bits / banda) + delay
    tempo_primeiro_chunk = (tamanho_chunk_base_bits / banda) + delay
    
    if perda > 0:
        tempo_primeiro_chunk *= (1 + (perda * 0.5))
    
    startup_delay = round(tempo_manifesto + tempo_primeiro_chunk, 3)
    
    # Simulação dos Chunks (Stalls e Resolução)
    tempo_total_travado = 0
    soma_resolucoes = 0
    
    for _ in range(total_chunks):
        if condicao_nome == "Oscilante":
            if protocolo == "MPEG-DASH":
                resolucao_atual = 480
                bitrate_atual = 1_200_000
            else:
                resolucao_atual = 720
                bitrate_atual = 2_500_000
        else:
            resolucao_atual = RESOLUCAO_BASE
            bitrate_atual = 4_000_000
            
        soma_resolucoes += resolucao_atual
        
        tamanho_chunk_bits = chunk_size * bitrate_atual
        tempo_download = (tamanho_chunk_bits / banda) + delay
        
        if perda > 0:
            tempo_download *= (1 + (perda * 0.3))
            
        if tempo_download > chunk_size:
            tempo_total_travado += (tempo_download - chunk_size)

    # Forçar o teto matemático lógico de 100% para o Stall Ratio
    stall_ratio = min(round((tempo_total_travado / DURACAO_VIDEO_S) * 100, 2), 100.0)
    resolucao_media = round(soma_resolucoes / total_chunks, 0)
    
    return startup_delay, stall_ratio, resolucao_media

# ==============================================================================
# ORQUESTRADOR
# ==============================================================================
print("🚀 Iniciando experimento com 10 repetições por cenário...")
with open('resultados_streaming.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Protocolo', 'Chunk_Size_S', 'Condicao_Rede', 'Repeticao', 'Startup_Delay_S', 'Stall_Ratio_Pct', 'Resolucao_Media_P'])
    
    for protocolo in PROTOCOLOS:
        for chunk_size in CHUNK_SIZES:
            for condicao, rede_config in CONDICOES_WAN.items():
                for rep in range(1, REPETICOES + 1):
                    startup, stall, res = simular_player_qoe(protocolo, chunk_size, condicao, rede_config)
                    writer.writerow([protocolo, chunk_size, condicao, rep, startup, stall, res])

print("🏁 Experimento concluído! Amostras salvas em 'resultados_streaming.csv'")
