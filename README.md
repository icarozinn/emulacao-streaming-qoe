# Avaliação de Desempenho e QoE: MPEG-DASH vs Apple-HLS

Este repositório contém o ambiente automatizado de testes e coleta de métricas de Qualidade de Experiência (QoE) para os protocolos de streaming adaptativo MPEG-DASH e Apple-HLS. O experimento foi desenvolvido em uma instância AWS EC2 (Ubuntu) utilizando a ferramenta Traffic Control (tc) do kernel do Linux para emulação de cenários de rede estáveis e oscilantes (WAN).

## 📊 O Experimento Fatorial (2x2x2)
O projeto analisa o comportamento dos protocolos sob as seguintes variáveis:
1. Protocolos: MPEG-DASH vs Apple-HLS
2. Tamanho do Chunk (Fragmento): 2 segundos vs 6 segundos
3. Condição da Rede WAN: Estável (sem restrições) vs Oscilante (2 Mbps de banda, 80ms de latência, 2% de perda de pacotes)

Para garantir o rigor científico, cada um dos 8 cenários foi executado por 15 repetições, totalizando 120 testes reais com Intervalo de Confiança de 95%.

---

## 🗂️ Estrutura dos Arquivos do Repositório

* emulacao_real.py: O orquestrador principal do experimento. Ele manipula o subsistema de rede do kernel via tc, faz as requisições HTTP reais de cada chunk de vídeo hospedado no servidor Apache local, cronometra o tempo de rede e calcula o Startup Delay e Stall Ratio empiricamente.
* experimento_script.py: Script da fase inicial do projeto. Funciona como um modelo analítico-estocástico rápido usado para validar a lógica matemática das heurísticas antes da emulação em tempo real.
* gerar_graficos.py: Script em Python (pandas e seaborn) que processa a base de dados gerada e plota os gráficos estatísticos com suas respectivas barras de erro (Intervalo de Confiança).
* resultados_streaming.csv: Base de dados crua contendo o log das 120 execuções reais coletadas direto da interface de rede.
* grafico_*.png: Gráficos gerados que demonstram o impacto do tamanho do chunk no atraso de inicialização e o colapso do buffering do HLS na rede instável.

---

## 🚀 Como Executar o Projeto

1. Instale as dependências de análise de dados:
   pip3 install pandas matplotlib seaborn requests --break-system-packages

2. Execute a emulação real (requer privilégios de root para alterar o tc do kernel):
   sudo python3 emulacao_real.py

3. Gere os gráficos estatísticos atualizados:
   python3 gerar_graficos.py

---
Ambiente de testes desenvolvido para fins acadêmicos na Universidade Federal do Ceará (UFC) - Campus Quixadá.
