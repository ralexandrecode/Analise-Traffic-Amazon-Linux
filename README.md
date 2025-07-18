# Analise-Traffic-Amazon-Linux
Código de script em Python usando Wireshark-CLI para monitorar o tráfego de entrada na instância Amazon Linux na Nuvem da AWS.

## Principais Funcionalidades do Script
Captura em tempo real - Salva dados conforme captura
Múltiplos formatos - Timestamp, IPs, portas, protocolos
Controle de duração - Por tempo ou número de pacotes
Análise básica - Estatísticas dos dados capturados
Tratamento de erros - Verifica permissões e instalações
Interrupção limpa - Ctrl+C para parar sem corromper arquivo
O script captura informações essenciais como origem, destino, 

## Código de arquivo Phyton

Baixe o arquivo script.py nesta página.
execute comando:
chmod +x script.py

### Script Python para Captura de Tráfego## Como usar o script
1. Salvar e dar permissões
# Salvar o script
nano traffic_capture.py

# Dar permissão de execução
chmod +x traffic_capture.py

2. Exemplos de uso
# Listar interfaces disponíveis
sudo python3 traffic_capture.py -l

# Captura básica na interface eth0
sudo python3 traffic_capture.py

# Captura por 60 segundos
sudo python3 traffic_capture.py -d 60

# Captura de 1000 pacotes
sudo python3 traffic_capture.py -c 1000

# Captura em interface específica
sudo python3 traffic_capture.py -i ens5

# Captura com arquivo personalizado
sudo python3 traffic_capture.py -o minha_captura.txt

# Analisar arquivo existente
python3 traffic_capture.py -a -o traffic_capture.txt
