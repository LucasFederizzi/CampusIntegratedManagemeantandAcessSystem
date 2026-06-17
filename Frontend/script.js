const API_URL = "http://127.0.0.1:5000/api/presenca";
const form = document.getElementById("attendance-form");
const messageEl = document.getElementById("message");
const presencasList = document.getElementById("presencasList");
const refreshButton = document.getElementById("refreshButton");

function setMessage(text, isError = false) {
  messageEl.textContent = text;
  messageEl.style.color = isError ? "#d64545" : "#1f44d8";
}

function formatDateTime(value) {
  const date = new Date(value);
  return date.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

async function fetchPresencas() {
  presencasList.innerHTML = "<p>Carregando...</p>";

  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error("Falha ao carregar registros");

    const presencas = await response.json();
    if (!Array.isArray(presencas) || presencas.length === 0) {
      presencasList.innerHTML = "<p>Nenhum registro encontrado.</p>";
      return;
    }

    const rows = presencas
      .slice()
      .reverse()
      .map(
        (registro) => `
        <tr>
          <td>${registro.id}</td>
          <td>${registro.nome}</td>
          <td>${formatDateTime(registro.hora)}</td>
          <td>${formatDateTime(registro.recebido_em)}</td>
        </tr>`
      )
      .join("");

    presencasList.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Hora</th>
            <th>Recebido em</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>`;
  } catch (error) {
    presencasList.innerHTML = "<p>Erro ao carregar registros. Verifique se o backend está rodando.</p>";
    console.error(error);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const cardId = document.getElementById("cardId").value.trim();
  const nome = document.getElementById("nome").value.trim();
  const hora = document.getElementById("hora").value;

  if (!cardId || !nome || !hora) {
    setMessage("Preencha todos os campos.", true);
    return;
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: cardId, nome, hora: new Date(hora).toISOString().slice(0, 19).replace("T", " ") }),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || "Erro no servidor");
    }

    setMessage("Presença registrada com sucesso.");
    form.reset();
    fetchPresencas();
  } catch (error) {
    setMessage(error.message, true);
    console.error(error);
  }
});

refreshButton.addEventListener("click", fetchPresencas);
window.addEventListener("load", fetchPresencas);
