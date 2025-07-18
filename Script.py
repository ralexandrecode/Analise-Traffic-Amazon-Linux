#!/usr/bin/env python3
"""
Script para capturar tráfego de rede usando TShark
Desenvolvido para Amazon Linux
Autor: Ricardo Alexandre + Claude4
Data: 18/07/2025
"""
import subprocess
import sys
import os
import signal
import datetime
import argparse
import json
import time

class TrafficCapture:
    def __init__(self, interface="eth0", output_file="traffic_capture.txt", duration=None, packet_count=None):
        """
        Inicializa o capturador de tráfego
        
        Args:
            interface (str): Interface de rede para capturar (padrão: eth0)
            output_file (str): Arquivo onde salvar os dados capturados
            duration (int): Duração em segundos para capturar (opcional)
            packet_count (int): Número de pacotes para capturar (opcional)
        """
        self.interface = interface
        self.output_file = output_file
        self.duration = duration
        self.packet_count = packet_count
        self.tshark_process = None
        self.capture_active = False
        
        # Configurar manipulador de sinal para interrupção limpa
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def check_permissions(self):
        """
        Verifica se o script está sendo executado com privilégios necessários
        """
        if os.geteuid() != 0:
            print("ERRO: Este script precisa ser executado com privilégios de root (sudo)")
            print("Execute: sudo python3 traffic_capture.py")
            sys.exit(1)
    
    def check_tshark_installed(self):
        """
        Verifica se o TShark está instalado no sistema
        """
        try:
            subprocess.run(['tshark', '--version'], 
                         capture_output=True, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERRO: TShark não encontrado!")
            print("Para Amazon Linux 2: sudo yum install wireshark")
            print("Para Amazon Linux 2023: sudo dnf install wireshark-cli")
            return False
    
    def list_interfaces(self):
        """
        Lista todas as interfaces de rede disponíveis
        """
        try:
            result = subprocess.run(['tshark', '-D'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            print("Interfaces disponíveis:")
            print(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Erro ao listar interfaces: {e}")
            return None
    
    def build_tshark_command(self):
        """
        Constrói o comando TShark baseado nos parâmetros fornecidos
        """
        # Comando base do TShark
        cmd = [
            'tshark',
            '-i', self.interface,  # Interface de rede
            '-T', 'fields',        # Formato de saída: campos
            '-e', 'frame.time',    # Timestamp do frame
            '-e', 'ip.src',        # IP de origem
            '-e', 'ip.dst',        # IP de destino
            '-e', 'tcp.srcport',   # Porta TCP de origem
            '-e', 'tcp.dstport',   # Porta TCP de destino
            '-e', 'udp.srcport',   # Porta UDP de origem
            '-e', 'udp.dstport',   # Porta UDP de destino
            '-e', '_ws.col.Protocol',  # Protocolo
            '-e', 'frame.len',     # Tamanho do frame
            '-E', 'header=y',      # Incluir cabeçalho
            '-E', 'separator=|',   # Separador de campos
            '-E', 'quote=d',       # Aspas duplas nos campos
            '-E', 'occurrence=f'   # Primeira ocorrência apenas
        ]
        
        # Adicionar limitação por tempo se especificado
        if self.duration:
            cmd.extend(['-a', f'duration:{self.duration}'])
        
        # Adicionar limitação por número de pacotes se especificado
        if self.packet_count:
            cmd.extend(['-c', str(self.packet_count)])
        
        return cmd
    
    def signal_handler(self, signum, frame):
        """
        Manipulador de sinais para interrupção limpa do programa
        """
        print(f"\nSinal {signum} recebido. Finalizando captura...")
        self.stop_capture()
        sys.exit(0)
    
    def start_capture(self):
        """
        Inicia a captura de tráfego de rede
        """
        print(f"Iniciando captura de tráfego...")
        print(f"Interface: {self.interface}")
        print(f"Arquivo de saída: {self.output_file}")
        if self.duration:
            print(f"Duração: {self.duration} segundos")
        if self.packet_count:
            print(f"Número de pacotes: {self.packet_count}")
        print("Pressione Ctrl+C para parar a captura\n")
        
        # Criar arquivo de saída com cabeçalho
        with open(self.output_file, 'w') as f:
            f.write(f"# Captura de Tráfego de Rede\n")
            f.write(f"# Iniciada em: {datetime.datetime.now()}\n")
            f.write(f"# Interface: {self.interface}\n")
            f.write(f"# Formato: Timestamp|IP_Origem|IP_Destino|Porta_TCP_Origem|Porta_TCP_Destino|Porta_UDP_Origem|Porta_UDP_Destino|Protocolo|Tamanho\n")
            f.write("#" + "="*100 + "\n")
        
        try:
            # Construir comando TShark
            cmd = self.build_tshark_command()
            
            # Iniciar processo TShark
            self.tshark_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )
            
            self.capture_active = True
            packet_count = 0
            
            # Ler saída em tempo real
            with open(self.output_file, 'a') as f:
                for line in iter(self.tshark_process.stdout.readline, ''):
                    if not self.capture_active:
                        break
                    
                    # Escrever linha no arquivo
                    f.write(line)
                    f.flush()  # Garantir que seja escrito imediatamente
                    
                    packet_count += 1
                    
                    # Mostrar progresso a cada 100 pacotes
                    if packet_count % 100 == 0:
                        print(f"Pacotes capturados: {packet_count}")
            
            # Aguardar finalização do processo
            self.tshark_process.wait()
            
        except Exception as e:
            print(f"Erro durante a captura: {e}")
        finally:
            self.stop_capture()
    
    def stop_capture(self):
        """
        Para a captura de tráfego
        """
        if self.tshark_process and self.tshark_process.poll() is None:
            print("Finalizando TShark...")
            self.tshark_process.terminate()
            
            # Aguardar até 5 segundos para finalização limpa
            try:
                self.tshark_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("TShark não finalizou limpo, forçando encerramento...")
                self.tshark_process.kill()
        
        self.capture_active = False
        
        # Adicionar informações de finalização ao arquivo
        if os.path.exists(self.output_file):
            with open(self.output_file, 'a') as f:
                f.write(f"\n# Captura finalizada em: {datetime.datetime.now()}\n")
        
        print(f"Captura salva em: {self.output_file}")
    
    def analyze_capture(self):
        """
        Análise básica do arquivo capturado
        """
        if not os.path.exists(self.output_file):
            print("Arquivo de captura não encontrado!")
            return
        
        print(f"\nAnálise do arquivo: {self.output_file}")
        print("-" * 50)
        
        try:
            with open(self.output_file, 'r') as f:
                lines = f.readlines()
            
            # Contar linhas de dados (excluindo comentários)
            data_lines = [line for line in lines if not line.startswith('#')]
            
            print(f"Total de pacotes capturados: {len(data_lines)}")
            print(f"Tamanho do arquivo: {os.path.getsize(self.output_file)} bytes")
            
            # Análise básica dos protocolos
            protocols = {}
            for line in data_lines:
                if '|' in line:
                    fields = line.split('|')
                    if len(fields) >= 8:
                        protocol = fields[7].strip()
                        protocols[protocol] = protocols.get(protocol, 0) + 1
            
            print("\nDistribuição de protocolos:")
            for protocol, count in sorted(protocols.items(), key=lambda x: x[1], reverse=True):
                if protocol:  # Ignorar protocolos vazios
                    print(f"  {protocol}: {count} pacotes")
                    
        except Exception as e:
            print(f"Erro na análise: {e}")

def main():
    """
    Função principal do script
    """
    parser = argparse.ArgumentParser(description="Capturador de Tráfego de Rede com TShark")
    parser.add_argument('-i', '--interface', default='eth0', 
                       help='Interface de rede para capturar (padrão: eth0)')
    parser.add_argument('-o', '--output', default='traffic_capture.txt', 
                       help='Arquivo de saída (padrão: traffic_capture.txt)')
    parser.add_argument('-d', '--duration', type=int, 
                       help='Duração da captura em segundos')
    parser.add_argument('-c', '--count', type=int, 
                       help='Número de pacotes para capturar')
    parser.add_argument('-l', '--list-interfaces', action='store_true', 
                       help='Listar interfaces disponíveis')
    parser.add_argument('-a', '--analyze', action='store_true', 
                       help='Analisar arquivo existente')
    
    args = parser.parse_args()
    
    # Criar instância do capturador
    capturer = TrafficCapture(
        interface=args.interface,
        output_file=args.output,
        duration=args.duration,
        packet_count=args.count
    )
    
    # Verificar instalação do TShark
    if not capturer.check_tshark_installed():
        sys.exit(1)
    
    # Listar interfaces se solicitado
    if args.list_interfaces:
        capturer.check_permissions()
        capturer.list_interfaces()
        return
    
    # Analisar arquivo existente se solicitado
    if args.analyze:
        capturer.analyze_capture()
        return
    
    # Verificar permissões para captura
    capturer.check_permissions()
    
    # Iniciar captura
    capturer.start_capture()

if __name__ == "__main__":
    main()
