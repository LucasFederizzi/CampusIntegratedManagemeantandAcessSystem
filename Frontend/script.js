const API_URL = "http://127.0.0.1:5000/api/presenca";
const presencasList = document.getElementById("presencasList");
const refreshButton = document.getElementById("refreshButton");

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
    setMessage("Falha ao carregar dados do hardware.", true);
    console.error(error);
  }
}

refreshButton.addEventListener("click", fetchPresencas);
window.addEventListener("load", fetchPresencas);
