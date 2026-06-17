# Frontend de Registro de Presença

Este frontend é uma página estática em HTML/CSS/JS que consome o backend Python.

## Como usar

1. Inicie o backend em `Backend/`:

```bash
cd Backend
python app.py
```

2. Em `Frontend/`, execute um servidor HTTP simples com Python:

```bash
cd Frontend
python -m http.server 8000
```

3. Abra o navegador em:

```text
http://127.0.0.1:8000
```

4. Registre presença preenchendo o formulário.

## Observações

- O frontend usa `fetch` para chamar `http://127.0.0.1:5000/api/presenca`.
- Certifique-se de que o backend esteja em execução antes de usar a aplicação.
