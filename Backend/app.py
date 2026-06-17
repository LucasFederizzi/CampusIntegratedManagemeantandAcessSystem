from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import sqlite3
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "presencas.db"


def get_db():
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presencas (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id TEXT NOT NULL,
            nome TEXT NOT NULL,
            hora TEXT NOT NULL,
            recebido_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TEXT
        )
    """)
    conn.commit()
    conn.close()


def row_to_dict(row):
    if not row:
        return None
    return dict(row)


def is_valid_payload(payload):
    return (
        isinstance(payload, dict)
        and "id" in payload
        and "nome" in payload
        and "hora" in payload
    )


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
init_db()


# CREATE - Registrar presença
@app.route("/api/presenca", methods=["POST"])
def registrar_presenca():
    payload = request.get_json(force=True, silent=True)
    if not payload or not is_valid_payload(payload):
        return jsonify({"error": "JSON inválido. Envie id, nome e hora."}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO presencas (card_id, nome, hora, recebido_em) VALUES (?, ?, ?, ?)",
        (str(payload["id"]), str(payload["nome"]), str(payload["hora"]), datetime.utcnow().isoformat() + "Z")
    )
    conn.commit()
    pk = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Presença registrada com sucesso",
        "pk": pk
    }), 201


# READ - Listar todas as presenças
@app.route("/api/presenca", methods=["GET"])
def listar_presencas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pk, card_id as id, nome, hora, recebido_em FROM presencas ORDER BY pk DESC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in rows]), 200


# READ - Buscar por ID
@app.route("/api/presenca/<int:pk>", methods=["GET"])
def obter_presenca(pk):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pk, card_id as id, nome, hora, recebido_em FROM presencas WHERE pk = ?", (pk,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Registro não encontrado"}), 404

    return jsonify(row_to_dict(row)), 200


# UPDATE - Atualizar presença
@app.route("/api/presenca/<int:pk>", methods=["PUT"])
def atualizar_presenca(pk):
    payload = request.get_json(force=True, silent=True)
    if not payload:
        return jsonify({"error": "JSON inválido"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pk FROM presencas WHERE pk = ?", (pk,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Registro não encontrado"}), 404

    updates = []
    params = []

    if "nome" in payload:
        updates.append("nome = ?")
        params.append(str(payload["nome"]))
    if "hora" in payload:
        updates.append("hora = ?")
        params.append(str(payload["hora"]))

    if not updates:
        conn.close()
        return jsonify({"error": "Nenhum campo para atualizar"}), 400

    updates.append("atualizado_em = ?")
    params.append(datetime.utcnow().isoformat() + "Z")
    params.append(pk)

    query = f"UPDATE presencas SET {', '.join(updates)} WHERE pk = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()

    return jsonify({"message": "Presença atualizada com sucesso"}), 200


# DELETE - Deletar presença
@app.route("/api/presenca/<int:pk>", methods=["DELETE"])
def deletar_presenca(pk):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT pk FROM presencas WHERE pk = ?", (pk,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Registro não encontrado"}), 404

    cursor.execute("DELETE FROM presencas WHERE pk = ?", (pk,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Presença deletada com sucesso"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
