# Guia de Configuracao do Hardware

## 1. Descobrir o IP do backend

No computador que roda `Backend/app.py`:

```powershell
ipconfig
```

No Linux, macOS ou Raspberry Pi:

```bash
hostname -I
```

Use o endereco IPv4 da rede local, por exemplo `192.168.1.50`.

## 2. Editar `config.py`

```python
BACKEND_HOST = "192.168.1.50"
BACKEND_PORT = 5000
```

## 3. Instalar dependencias

```bash
cd Hardware
pip install -r requirements.txt
```

## 4. Testar HTTP

Com o backend rodando:

```bash
python http_sender.py
```

Resposta esperada:

```text
[HTTP] Enviando: {'id': '1234567890', 'hora': '...'}
Sucesso! PK: 1
```

## 5. Testar RFID serial

```bash
python rfid_reader.py
```

Passe um cartao no leitor e confira o registro pelo endpoint:

```bash
curl http://192.168.1.50:5000/api/presenca
```

## Troubleshooting

| Erro | Solucao |
|------|---------|
| `Falha ao conectar` | IP incorreto em `config.py` |
| `Connection refused` | Backend nao esta rodando |
| `Serial port not found` | Altere `SERIAL_PORT` em `config.py` |

Para descobrir a porta serial:

```bash
python -m serial.tools.list_ports
```
