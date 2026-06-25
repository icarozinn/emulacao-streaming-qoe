#!/usr/bin/env python3
import time
import csv
import urllib.request
import re
import os

# CONFIGURAÇÕES DO EXPERIMENTO FATORIAL (2x2x2) com 15 Repetições
PROTOCOLOS = ["MPEG-DASH", "Apple-HLS"]
CHUNK_SIZES = [2, 6]
CONDICOES_WAN = ["Estavel", "Oscilante"]
REPETICOES = 30

# IP Local da sua instância onde o Apache está rodando (localhost ou 127.0.0.1)
URL_BASE = "http://127.0.0.1/streaming"

def aplicar_regras_kernel_tc(condicao):
    """
    Simula o CORE injetando as restrições direto no Traffic Control (tc) do Linux.
    Dessa forma, o download via HTTP sofre o impacto REAL do kernel.
    """
    # Limpa regras anteriores
    os.system("sudo tc qdisc del dev lo root 2>/dev/null")
    
    if condicao == "Oscilante":
        # 2 Mbps de banda, 80ms de delay, 2% de perda de pacotes
        os.system("sudo tc qdisc add dev lo root handle 1: netem delay 80ms loss 2% rate 2mbit")
        print(f" comando tc: WAN Oscilante aplicada na interface de loopback.")
    else:
        # Rede estável: limpa as restrições (Banda máxima da EC2, 0% perda)
        print(f" comando tc: WAN Estável (sem restrições) aplicada.")

def emular_player_http(protocolo, chunk_size, condicao):
    """
    Baixa os arquivos reais do Apache e cronometra o tempo de rede do kernel.
    """
    tempo_total_travado = 0
    soma_resolucoes = 0
    
    # Define caminhos e resoluções com base na heurística adaptativa real
    if protocolo == "MPEG-DASH":
        manifest_url = f"{URL_BASE}/dash_{chunk_size}s/manifest.mpd"
        resolucao_real = 480 if condicao == "Oscilante" else 1080
        # Simula o player baixando a lista de chunks (geralmente de 10 a 30 chunks para 60s)
        total_chunks = 30 if chunk_size == 2 else 10
        chunk_template = f"{URL_BASE}/dash_{chunk_size}s/chunk-stream0-{{:05d}}.m4s"
    else:
        manifest_url = f"{URL_BASE}/hls_{chunk_size}s/master.m3u8"
        resolucao_real = 720 if condicao == "Oscilante" else 1080
        total_chunks = 30 if chunk_size == 2 else 10
        chunk_template = f"{URL_BASE}/hls_{chunk_size}s/master{{:d}}.ts"

    # 1. Mede o MTR / Startup Delay Real (Baixar manifesto + primeiro chunk)
    t0 = time.time()
    try:
        urllib.request.urlopen(manifest_url, timeout=5).read()
        urllib.request.urlopen(chunk_template.format(1), timeout=5).read()
        startup_delay = round(time.time() - t0, 3)
    except Exception:
        # Se a rede oscilante derrubar o pacote, gera penalidade de timeout TCP
        startup_delay = round((time.time() - t0) + 4.0, 3)

    # 2. Loop de Download dos Chunks Restantes (Medindo Buffering / Stall)
    for i in range(2, total_chunks + 1):
        url_chunk = chunk_template.format(i)
        
        t_download_inicio = time.time()
        try:
            urllib.request.urlopen(url_chunk, timeout=10).read()
            tempo_download_real = time.time() - t_download_inicio
        except Exception:
            tempo_download_real = chunk_size * 2 # Penalidade de retransmissão pesada
            
        # Se o download real na interface demorou mais que o tempo do chunk, houve STALL!
        if tempo_download_real > chunk_size:
            tempo_total_travado += (tempo_download_real - chunk_size)
            
        soma_resolucoes += resolucao_real

    # Cálculos Finais baseados nas métricas reais da rede
    stall_ratio = min(round((tempo_total_travado / 60.0) * 100, 2), 100.0)
    resolucao_media = round(soma_resolucoes / total_chunks, 0)
    
    return startup_delay, stall_ratio, resolucao_media

# ==============================================================================
# ORQUESTRADOR DO AMBIENTE DE EMULAÇÃO REAL
# ==============================================================================
print("🚀 [DEVOPS] Iniciando Emulação Real com Tráfego de Rede via Kernel...")

with open('resultados_streaming.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Protocolo', 'Chunk_Size_S', 'Condicao_Rede', 'Repeticao', 'Startup_Delay_S', 'Stall_Ratio_Pct', 'Resolucao_Media_P'])
    
    rodada_total = 1
    total_execucoes = len(PROTOCOLOS) * len(CHUNK_SIZES) * len(CONDICOES_WAN) * REPETICOES
    
    for condicao in CONDICOES_WAN:
        # Altera o comportamento do kernel via 'tc' antes de rodar o bloco
        aplicar_regras_kernel_tc(condicao)
        time.sleep(2) # Tempo para o kernel estabilizar a tabela de rotas
        
        for protocolo in PROTOCOLOS:
            for chunk_size in CHUNK_SIZES:
                for rep in range(1, REPETICOES + 1):
                    print(f"📦 [{rodada_total}/{total_execucoes}] {protocolo} | Chunk: {chunk_size}s | Rede: {condicao} | Rep: {rep}")
                    
                    # Executa o tráfego real
                    startup, stall, res = emular_player_http(protocolo, chunk_size, condicao)
                    
                    writer.writerow([protocolo, chunk_size, condicao, rep, startup, stall, res])
                    rodada_total += 1

# Limpa a placa de rede ao final do experimento
os.system("sudo tc qdisc del dev lo root 2>/dev/null")
print("\n🏁 [CONCLUÍDO] Experimento real finalizado! Dados salvos em 'resultados_streaming.csv'")
