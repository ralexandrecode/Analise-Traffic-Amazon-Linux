# 🌐 Traffic Capture Tools

Conjunto de ferramentas para captura e análise de tráfego de rede usando **TShark** e **Python**.

## 📋 Descrição

Este projeto fornece scripts e ferramentas para:
- Capturar tráfego de rede em tempo real
- Analisar dados de rede salvos
- Gerar relatórios de tráfego
- Monitorar atividade de rede

## 🚀 Funcionalidades

- ✅ Captura em tempo real com TShark
- ✅ Análise básica de protocolos
- ✅ Exportação para arquivo de texto
- ✅ Controle de duração e quantidade
- ✅ Interrupção limpa (Ctrl+C)
- ✅ Verificação de permissões
- ✅ Suporte ao Amazon Linux

## 📦 Instalação

### Pré-requisitos

```bash
# Amazon Linux 2
sudo yum update
sudo yum install python3 wireshark

# Amazon Linux 2023
sudo dnf install python3 wireshark-cli
```

### Instalação do projeto

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/traffic-capture-tools.git
cd traffic-capture-tools

# Dar permissões de execução
chmod +x traffic_capture.py

# Verificar instalação
python3 traffic_capture.py --help
```

## 🛠️ Uso

### Comandos básicos

```bash
# Listar interfaces disponíveis
sudo python3 traffic_capture.py -l

# Captura básica (pressione Ctrl+C para parar)
sudo python3 traffic_capture.py

# Captura por tempo limitado (60 segundos)
sudo python3 traffic_capture.py -d 60

# Captura número específico de pacotes
sudo python3 traffic_capture.py -c 1000
```

### Exemplos avançados

```bash
# Captura em interface específica
sudo python3 traffic_capture.py -i ens5

# Salvar em arquivo personalizado
sudo python3 traffic_capture.py -o minha_captura.txt

# Captura longa com análise automática
sudo python3 traffic_capture.py -d 300 -o captura_5min.txt
python3 traffic_capture.py -a -o captura_5min.txt
```

## 📊 Análise dos Dados

O script gera arquivos de texto com o seguinte formato:

```
# Captura de Tráfego de Rede
# Timestamp|IP_Origem|IP_Destino|Porta_TCP_Origem|Porta_TCP_Destino|Porta_UDP_Origem|Porta_UDP_Destino|Protocolo|Tamanho
"2025-07-18 14:30:15"|"192.168.1.100"|"8.8.8.8"|""|""|"53"|"53"|"DNS"|"64"
"2025-07-18 14:30:16"|"192.168.1.100"|"142.250.191.14"|"443"|"443"|""|""|"TLS"|"1420"
```

### Análise automática

```bash
# Analisar arquivo capturado
python3 traffic_capture.py -a -o traffic_capture.txt
```

**Saída exemplo:**
```
Análise do arquivo: traffic_capture.txt
--------------------------------------------------
Total de pacotes capturados: 1500
Tamanho do arquivo: 125000 bytes

Distribuição de protocolos:
  HTTP: 850 pacotes
  HTTPS: 400 pacotes
  DNS: 180 pacotes
  SSH: 70 pacotes
```

## 🔧 Parâmetros

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `-i, --interface` | Interface de rede | `-i eth0` |
| `-o, --output` | Arquivo de saída | `-o captura.txt` |
| `-d, --duration` | Duração em segundos | `-d 300` |
| `-c, --count` | Número de pacotes | `-c 1000` |
| `-l, --list-interfaces` | Listar interfaces | `-l` |
| `-a, --analyze` | Analisar arquivo | `-a` |

## 📁 Estrutura do Projeto

```
traffic-capture-tools/
├── README.md
├── traffic_capture.py
├── examples/
│   ├── basic_capture.sh
│   └── advanced_analysis.py
├── docs/
│   ├── installation.md
│   └── troubleshooting.md
└── tests/
    └── test_capture.py
```

## 🐛 Troubleshooting

### Problemas comuns

**Erro de permissão:**
```bash
# Executar com sudo
sudo python3 traffic_capture.py
```

**TShark não encontrado:**
```bash
# Amazon Linux 2
sudo yum install wireshark

# Amazon Linux 2023
sudo dnf install wireshark-cli
```

**Interface não encontrada:**
```bash
# Listar interfaces disponíveis
sudo python3 traffic_capture.py -l
```

### Logs de erro

Os logs detalhados são salvos em `/var/log/traffic_capture.log` (se executado como root).

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de código

- Use **PEP 8** para Python
- Documente todas as funções
- Adicione testes para novas funcionalidades
- Use mensagens de commit descritivas

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvimento inicial* - [seu-usuario](https://github.com/seu-usuario)

## 📞 Suporte

- 📧 Email: seu-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/traffic-capture-tools/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/seu-usuario/traffic-capture-tools/wiki)

## 🔄 Changelog

### v1.0.0 - 2025-07-18
- ✅ Primeira versão estável
- ✅ Captura básica de tráfego
- ✅ Análise automática
- ✅ Suporte ao Amazon Linux

### v0.9.0 - 2025-07-15
- ✅ Versão beta
- ✅ Funcionalidades básicas implementadas

## 🙏 Agradecimentos

- Equipe do [Wireshark](https://www.wireshark.org/) pelo TShark
- Comunidade Python
- Documentação do Amazon Linux
