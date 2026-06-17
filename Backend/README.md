# Backend de Registro de Presença

Backend Flask com SQLite para registrar presença enviada por hardware (Raspberry Pi + Arduino com RFID).

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints CRUD

### CREATE - Registrar presença
```bash
POST /api/presenca
Content-Type: application/json

{
  "id": "1234567890",
  "nome": "João Silva",
  "hora": "2026-06-16 14:30:00"
}
```

### READ - Listar todas
```bash
GET /api/presenca
```

### READ - Buscar por PK
```bash
GET /api/presenca/1
```

### UPDATE - Atualizar registro
```bash
PUT /api/presenca/1
Content-Type: application/json

{
  "nome": "João Silva Atualizado",
  "hora": "2026-06-16 15:00:00"
}
```

### DELETE - Deletar registro
```bash
DELETE /api/presenca/1
```

## Banco de Dados

- Arquivo: `Backend/data/presencas.db`
- Tabela: `presencas` com campos `pk`, `card_id`, `nome`, `hora`, `recebido_em`, `atualizado_em`
