const API_URL = "http://127.0.0.1:5000/api/presenca";
const LATEST_URL = API_URL;
const ACTIVE_URL = "http://127.0.0.1:5000/api/emprestimos/ativos";
const latestEl = document.getElementById("latest");
const confirmBtn = document.getElementById("confirmBtn");
const recipientName = document.getElementById("recipientName");
const cardSearch = document.getElementById("cardSearch");
const searchBtn = document.getElementById("searchBtn");
const currentLoansEl = document.getElementById("currentLoans");
const historyListEl = document.getElementById("historyList");

let latestRecord = null;

function formatDateTime(value) {
  if (!value) return "-";
  const d = new Date(value);
  if (isNaN(d)) return String(value);
  return d.toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" });
}

async function loadLatest() {
  latestEl.innerHTML = "Carregando...";
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error('falha');
    const items = await res.json();
    if (!Array.isArray(items) || items.length === 0) {
      latestEl.innerHTML = '<p>Nenhum registro.</p>';
      latestRecord = null;
      return;
    }

    const latest = items.slice().reverse()[0] || items[0];
    latestRecord = latest;

    const id = latest.id || latest.card_id || latest.uid || '-';
    const hora = latest.hora || latest.timestamp || latest.recebido_em || '-';
    const bookCode = latest.book_code || latest.codigo_livro || latest.local || '-';

    latestEl.innerHTML = `
      <table>
        <tbody>
          <tr><th>ID</th><td>${id}</td></tr>
          <tr><th>Hora</th><td>${formatDateTime(hora)}</td></tr>
          <tr><th>Código do Livro</th><td>${bookCode}</td></tr>
        </tbody>
      </table>`;
  } catch (err) {
    latestEl.innerHTML = '<p>Erro ao carregar.</p>';
    console.error(err);
  }
}

confirmBtn.addEventListener('click', async () => {
  if (!latestRecord) return alert('Nenhum registro para confirmar.');

  const id = latestRecord.id || latestRecord.card_id || latestRecord.uid || null;
  const horaRaw = latestRecord.hora || latestRecord.timestamp || latestRecord.recebido_em || new Date().toISOString();
  const hora = new Date(horaRaw).toISOString().slice(0,19).replace('T',' ');
  const nome = recipientName.value.trim() || '';
  const bookCode = latestRecord.book_code || latestRecord.codigo_livro || latestRecord.local || null;

  if (!id) return alert('Registro inválido, sem ID.');

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, nome: nome || 'Desconhecido', hora, book_code: bookCode, tipo: 'borrow' })
    });

    if (!res.ok) {
      const data = await res.json().catch(()=>({}));
      throw new Error(data.error || 'Erro ao confirmar');
    }

    alert('Recebimento confirmado.');
    recipientName.value = '';
    loadLatest();
    // if a card id is in the search box, refresh its lists
    if (cardSearch.value.trim()) fetchUserData(cardSearch.value.trim());
  } catch (err) {
    console.error(err);
    alert('Falha ao confirmar recebimento.');
  }
});

async function fetchUserData(cardId) {
  // current loans
  currentLoansEl.innerHTML = 'Carregando...';
  historyListEl.innerHTML = 'Carregando...';
  try {
    const [activeRes, histRes] = await Promise.all([
      fetch(ACTIVE_URL),
      fetch(`${API_URL}/usuario/${encodeURIComponent(cardId)}`),
    ]);

    if (activeRes.ok) {
      const active = await activeRes.json();
      const mine = (active || []).filter(a => String(a.id) === String(cardId));
      if (!mine.length) currentLoansEl.innerHTML = '<p>Sem livros emprestados no momento.</p>';
      else {
        const rows = mine.map(m => `
          <tr>
            <td>${m.book_code || m.local || '-'}</td>
            <td>${formatDateTime(m.hora)}</td>
            <td><button data-book="${m.book_code || m.local || ''}" data-id="${m.id}">Confirmar devolução</button></td>
          </tr>`).join('');
        currentLoansEl.innerHTML = `
          <table>
            <thead><tr><th>Código</th><th>Hora</th><th>Ação</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>`;

        // attach return handlers
        currentLoansEl.querySelectorAll('button[data-book]').forEach(b => {
          b.addEventListener('click', async (e) => {
            const book = b.getAttribute('data-book');
            const id = b.getAttribute('data-id');
            if (!confirm('Confirmar devolução do livro ' + book + '?')) return;
            try {
              const horaNow = new Date().toISOString().slice(0,19).replace('T',' ');
              const res = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, nome: recipientName.value.trim() || 'Desconhecido', hora: horaNow, book_code: book, tipo: 'return' })
              });
              if (!res.ok) throw new Error('Erro');
              alert('Devolução registrada.');
              fetchUserData(cardId);
            } catch (err) { console.error(err); alert('Falha ao registrar devolução.'); }
          });
        });
      }
    } else {
      currentLoansEl.innerHTML = '<p>Erro ao carregar empréstimos ativos.</p>';
    }

    if (histRes.ok) {
      const hist = await histRes.json();
      if (!Array.isArray(hist) || hist.length === 0) historyListEl.innerHTML = '<p>Nenhum histórico encontrado.</p>';
      else {
        const rows = hist.map(h => `
          <tr>
            <td>${h.book_code || h.local || '-'}</td>
            <td>${h.tipo || '-'}</td>
            <td>${formatDateTime(h.hora)}</td>
            <td>${formatDateTime(h.recebido_em)}</td>
          </tr>`).join('');
        historyListEl.innerHTML = `
          <table>
            <thead><tr><th>Código</th><th>Tipo</th><th>Hora</th><th>Recebido em</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>`;
      }
    } else {
      historyListEl.innerHTML = '<p>Erro ao carregar histórico.</p>';
    }
  } catch (err) {
    console.error(err);
    currentLoansEl.innerHTML = '<p>Erro ao carregar dados.</p>';
    historyListEl.innerHTML = '<p>Erro ao carregar dados.</p>';
  }
}

searchBtn.addEventListener('click', () => {
  const id = cardSearch.value.trim();
  if (!id) return alert('Digite um ID de cartão.');
  fetchUserData(id);
});

window.addEventListener('load', () => {
  loadLatest();
  setInterval(loadLatest, 8000);
});
