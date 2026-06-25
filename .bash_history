sudo apt update
sudo apt upgrade
sudo apt install -y curl git python3-pip python3-venv \ libev-dev bash bridge-utils iproute2 ebtables iptables wmediumd
sudo add-apt-repository universe
sudo apt update
sudo apt install -y curl git python3-pip python3-venv libev-dev bash bridge-utils iproute2 ebtables iptables wmediumd
sudo apt install -y curl git python3-pip python3-venv libev-dev bash bridge-utils iproute2 ebtables iptables libnl-3-dev libnl-genl-3-dev
# 1. Clonar o repositório oficial
git clone https://github.com/coreemu/core.git
cd core
# 2. Instalar a ferramenta que roda a instalação
sudo apt install -y python3-invoke
# 3. Rodar a instalação automática do CORE
sudo inv install
sudo apt install -y python3-invoke
sudo inv install
sudo apt install -y automake libtool split-select pkg-config
./setup.sh
sudo inv install
sudo pip3 install poetry --break-system-packages
sudo inv install
sudo pip3 install poetry --break-system-packages --ignore-installed urllib3
sudo inv install
sudo systemctl start core-daemon
sudo systemctl enable core-daemon
sudo systemctl status core-daemon
pip3 install pandas matplotlib seaborn --break-system-packages
nano gerar_graficos.py
python3 gerar_graficos.py 
ls
sudo apt update
sudo apt install -y ffmpeg apache2
sudo mkdir -p /var/www/html/streaming
sudo chown -R ubuntu:ubuntu /var/www/html/streaming
cd /var/www/html/streaming
curl -L -o teste.mp4 https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_5MB.mp4
mkdir -p dash_2s dash_6s hls_2s hls_6s
ls
ffmpeg -i teste.mp4 -c:v copy -c:a copy -f dash -seg_duration 2 dash_2s/manifest.mpd
ffmpeg -i teste.mp4 -c:v copy -c:a copy -f dash -seg_duration 6 dash_6s/manifest.mpd
ffmpeg -i teste.mp4 -c:v copy -c:a copy -f hls -hls_time 2 -hls_playlist_type vod hls_2s/master.m3u8
ffmpeg -i teste.mp4 -c:v copy -c:a copy -f hls -hls_time 6 -hls_playlist_type vod hls_6s/master.m3u8
ls
cd dash_2s/
ls
cd ;;
cd ..
cd
nano experimento_script.py
chmod +x experimento_script.py 
python3 experimento_script.py 
sudo /opt/core/venv/bin/python3 experimento_script.py
nano experimento_script.py
python3 experimento_script.py 
sudo /opt/core/venv/bin/python3 experimento_script.py
nano experimento_script.py
python3 experimento_script.py 
column -s, -t < resultados_streaming.csv
nano experimento_script.py 
python3 experimento_script.py
nano experimento_script.py 
python3 experimento_script.py
column -s, -t < resultados_streaming.csv
nano gerar_graficos.py
python3 gerar_graficos.py
ls
cd /var/www/html/streaming/
curl -L -o teste_60s.mp4 https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_60s_50MB.mp4
ffmpeg -y -i teste_60s.mp4 -c:v copy -c:a copy -f dash -seg_duration 2 dash_2s/manifest.mpd
rm -f teste_60s.mp4 
ls
wget -O teste_60s.mp4 https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4
ffmpeg -y -i teste_60s.mp4 -c:v copy -c:a copy -f dash -seg_duration 2 dash_2s/manifest.mpd
# MPEG-DASH (2s e 6s)
ffmpeg -y -i teste_60s.mp4 -t 60 -c:v copy -c:a copy -f dash -seg_duration 2 dash_2s/manifest.mpd
ffmpeg -y -i teste_60s.mp4 -t 60 -c:v copy -c:a copy -f dash -seg_duration 6 dash_6s/manifest.mpd
# Apple HLS (2s e 6s)
ffmpeg -y -i teste_60s.mp4 -t 60 -c:v copy -c:a copy -f hls -hls_time 2 -hls_playlist_type vod hls_2s/master.m3u8
ffmpeg -y -i teste_60s.mp4 -t 60 -c:v copy -c:a copy -f hls -hls_time 6 -hls_playlist_type vod hls_6s/master.m3u8
cd
nano emulacao_real.py
pip3 install requests --break-system-packages
sudo python3 emulacao_real.py 
ls
python3 gerar_graficos.py 
ls
history
ls
chmod +x experimento_script.py 
ls
nano README.md
ls
echo "core/" > .gitignore
echo "ospf-mdr/" >> .gitignore
echo "teste_60s.mp4" >> .gitignore
git init
git add emulacao_real.py gerar_graficos.py experimento_script.py resultados_streaming.csv grafico_*.png .gitignore README.md 
git commit -m "feat: ambiente de emulacao real de QoE e graficos com IC 95%"
git checkout -b main
git remote add origin https://github.com/icarozinn
git push -u origin main
git remote add origin https://github.com/icarozinn/emulacao-streaming-qoe.git
git push -u origin main
git remote remove origin
git remote add origin https://github.com/icarozinn/emulacao-streaming-qoe.git
git push -u origin main
git remote add origin https://github.com/icarozinn/emulacao-streaming-qoe.git
git push -u origin main
ls
nano emulacao_real.py 
ls
chmod +x emulacao_real.py 
python3 emulacao_real.py 
HISTTIMEFORMAT="%d/%m/%y %H:%M:%S " history
ls
python3 gerar_graficos.py 
cat resultados_streaming.csv 
ls
nano gerar_graficos.py 
chmod +x gerar_graficos.py 
python3 gerar_graficos.py 
ls
nano gerar_graficos.py 
python3 gerar_graficos.py 
ls
rm grafico_resolucao_media.png 
ls
rm grafico_stall_ratio.png 
rm grafico_startup_delay.png 
ls
