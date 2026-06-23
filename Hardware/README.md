# Conexao Raspberry Pi + Arduino + RFID

O hardware envia leituras RFID ao backend somente via HTTP POST.

## Configuracao

Edite `Hardware/config.py` com o IP do computador que esta rodando o backend:

```python
BACKEND_HOST = "192.168.1.100"
BACKEND_PORT = 5000
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/presenca"

SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BAUD_RATE = 9600
```

Para descobrir o IP do backend:

- Windows: `ipconfig`
- Linux, macOS ou Raspberry Pi: `hostname -I`

Use um IP da rede local, nao `127.0.0.1`, quando a Raspberry Pi estiver em outra maquina.

## Arquitetura

```text
Raspberry Pi / Arduino / RFID
    -> HTTP POST /api/presenca
    -> Backend Flask
    -> SQLite
```

## Instalacao

```bash
cd Hardware
pip install -r requirements.txt
```

## Testar envio HTTP

```bash
python http_sender.py
```

O backend deve responder com status `201` e o `pk` do registro criado.

## Rodar leitor RFID

```bash
python rfid_reader.py
```

Se estiver usando o script simples antigo:

```bash
python RaspberryPi.py
```

## Payload esperado pelo backend

```json
{
  "id": "1234567890",
  "nome": "Usuario RFID",
  "hora": "2026-06-23 14:30:00",
  "book_code": "LIV001",
  "tipo": "entrada"
}
```

`id` e `hora` sao obrigatorios. Os campos `nome`, `book_code` e `tipo` sao opcionais.

## Verificar registros

```bash
curl http://192.168.1.100:5000/api/presenca
```

Ou abra o frontend apontando para o mesmo backend.

## Troubleshooting

| Erro | Solucao |
|------|---------|
| `Falha ao conectar` | Verifique `BACKEND_HOST` em `config.py` |
| `Connection refused` | Inicie o backend Flask |
| `Serial port not found` | Ajuste `SERIAL_PORT` em `config.py` |

Para listar portas seriais:

```bash
python -m serial.tools.list_ports
```
