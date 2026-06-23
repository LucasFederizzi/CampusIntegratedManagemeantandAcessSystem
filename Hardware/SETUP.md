# 🚀 Guia Completo de Configuração

## Passo 1: Descobrir o IP do Backend

### Windows
```powershell
ipconfig
```
Procure por: `IPv4 Address` (não 127.0.0.1)

### Linux / Mac / Raspberry Pi
```bash
hostname -I
```

**Exemplo de resultado:**
```
192.168.1.50
```

## Passo 2: Editar config.py

Na Raspberry Pi, abra `Hardware/config.py` e altere:

```python
# ← AQUI! Cole o IP que você descobriu
BACKEND_HOST = "192.168.1.50"  
```

## Passo 3: Testá Conexão

### Teste 1: HTTP

```bash
cd Hardware
python http_sender.py
```

**Esperado:**
```
[HTTP] Enviando: {'id': '1234567890', 'nome': 'Usuário RFID', 'hora': '...'}
✓ 1234567890 registrado (PK: 1)
```

### Teste 2: RabbitMQ (opcional)

```bash
python rabbitmq_sender.py
```

**Esperado:**
```
[RabbitMQ] Conectando em 192.168.1.50...
✓ Mensagem publicada na fila 'presencas'
```

### Teste 3: RFID Serial (com Arduino)

```bash
python rfid_reader.py
```

**Aguarde e passe um cartão no leitor...**

## Passo 4: Verificar Backend

Vá para o computador rodando o backend e verifique:

### Via API
```bash
curl http://192.168.1.50:5000/api/presenca
```

### Via Frontend
```
http://192.168.1.50:8000
```

## Troubleshooting

| Erro | Solução |
|------|---------|
| `Falha ao conectar` | IP incorreto em `config.py` |
| `Connection refused` | Backend não está rodando |
| `Serial port not found` | Altere `SERIAL_PORT` em `config.py` |
| `RabbitMQ error` | RabbitMQ não está rodando |

### Descobrir porta serial

```bash
python -m serial.tools.list_ports
```

## Resumo Rápido

1. Descubra IP do backend: `ipconfig` ou `hostname -I`
2. Edite `config.py` com o IP
3. Rodezinho com `python http_sender.py`
4. Pronto! Dados vão pro banco de dados automaticamente
