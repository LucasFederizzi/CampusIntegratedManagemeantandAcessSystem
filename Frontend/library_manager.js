const API_URL = "http://127.0.0.1:5000/api/presenca";
const BOOKS_API = "http://127.0.0.1:5000/api/books";
const managerList = document.getElementById('managerList');
const refreshBtn = document.getElementById('refreshButton');
const searchInput = document.getElementById('searchInput');
const booksListEl = document.getElementById('booksList');
const addBookForm = document.getElementById('addBookForm');
const bookCodeInput = document.getElementById('bookCode');
const bookTitleInput = document.getElementById('bookTitle');
const bookAuthorInput = document.getElementById('bookAuthor');
const bookCopiesInput = document.getElementById('bookCopies');

function formatDateTime(value) {
  if (!value) return '-';
  const d = new Date(value);
  if (isNaN(d)) return String(value);
  return d.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

async function loadRecords() {
  managerList.innerHTML = 'Carregando...';
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error('falha');
    const items = await res.json();
    renderTable(items);
    // also refresh books
    loadBooks();
  } catch (err) {
    managerList.innerHTML = '<p>Erro ao carregar registros.</p>';
    console.error(err);
  }
}

function renderTable(items) {
  const q = searchInput.value.trim().toLowerCase();
  const rows = (Array.isArray(items) ? items : [])
    .slice()
    .reverse()
    .filter(i => {
      if (!q) return true;
      const id = String(i.id || i.card_id || i.uid || '');
      const nome = String(i.nome || '');
      return id.toLowerCase().includes(q) || nome.toLowerCase().includes(q);
    })
    .map(i => {
      const pk = i.pk || i.pk;
      const id = i.id || i.card_id || i.uid || '-';
      const nome = i.nome || '-';
      const hora = i.hora || i.timestamp || i.recebido_em || '-';
      return `
        <tr>
          <td>${pk || '-'}</td>
          <td>${id}</td>
          <td>${nome}</td>
          <td>${formatDateTime(hora)}</td>
          <td>
            <button data-action="edit" data-pk="${pk}">Editar</button>
            <button data-action="delete" data-pk="${pk}">Excluir</button>
          </td>
        </tr>`;
    }).join('');

  managerList.innerHTML = `
    <table>
      <thead>
        <tr><th>PK</th><th>ID</th><th>Nome</th><th>Hora</th><th>Ações</th></tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;

  // attach handlers
  managerList.querySelectorAll('button[data-action]').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const action = btn.getAttribute('data-action');
      const pk = btn.getAttribute('data-pk');
      if (action === 'delete') return handleDelete(pk);
      if (action === 'edit') return handleEdit(pk);
    });
  });
}

async function handleDelete(pk) {
  if (!confirm('Confirma exclusão do registro ' + pk + '?')) return;
  try {
    const res = await fetch(`${API_URL}/${pk}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Erro ao excluir');
    loadRecords();
  } catch (err) {
    alert('Falha ao excluir. Veja console para detalhes.');
    console.error(err);
  }
}

async function handleEdit(pk) {
  const nome = prompt('Novo nome:');
  if (nome === null) return;
  const hora = prompt('Nova hora (YYYY-MM-DD HH:MM:SS) — deixe em branco para manter:');
  const payload = {};
  if (nome) payload.nome = nome;
  if (hora) payload.hora = hora;
  if (Object.keys(payload).length === 0) return;

  try {
    const res = await fetch(`${API_URL}/${pk}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const data = await res.json().catch(()=>({}));
      throw new Error(data.error || 'Erro ao atualizar');
    }
    loadRecords();
  } catch (err) {
    alert('Falha ao atualizar. Veja console.');
    console.error(err);
  }
}

refreshBtn.addEventListener('click', loadRecords);
searchInput.addEventListener('input', () => loadRecords());
window.addEventListener('load', loadRecords);

// BOOKS: list, add, edit, delete
async function loadBooks() {
  booksListEl.innerHTML = 'Carregando...';
  try {
    const res = await fetch(BOOKS_API);
    if (!res.ok) throw new Error('falha books');
    const books = await res.json();
    renderBooks(books);
  } catch (err) {
    booksListEl.innerHTML = '<p>Erro ao carregar livros.</p>';
    console.error(err);
  }
}

function renderBooks(books) {
  const rows = (Array.isArray(books) ? books : [])
    .map(b => `
      <tr>
        <td>${b.id}</td>
        <td>${b.code || '-'}</td>
        <td>${b.title}</td>
        <td>${b.author || '-'}</td>
        <td>${b.copies || 1}</td>
        <td>
          <button data-book-action="edit" data-id="${b.id}">Editar</button>
          <button data-book-action="delete" data-id="${b.id}">Excluir</button>
        </td>
      </tr>`).join('');

  booksListEl.innerHTML = `
    <table>
      <thead><tr><th>ID</th><th>Código</th><th>Título</th><th>Autor</th><th>Cópias</th><th>Ações</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>`;

  booksListEl.querySelectorAll('button[data-book-action]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const action = btn.getAttribute('data-book-action');
      const id = btn.getAttribute('data-id');
      if (action === 'delete') return deleteBook(id);
      if (action === 'edit') return editBookPrompt(id);
    });
  });
}

addBookForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    code: bookCodeInput.value.trim() || null,
    title: bookTitleInput.value.trim(),
    author: bookAuthorInput.value.trim() || null,
    copies: parseInt(bookCopiesInput.value, 10) || 1
  };
  try {
    const res = await fetch(BOOKS_API, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const data = await res.json().catch(()=>({}));
      throw new Error(data.error || 'Erro ao adicionar livro');
    }
    bookCodeInput.value = ''; bookTitleInput.value = ''; bookAuthorInput.value = ''; bookCopiesInput.value = '';
    loadBooks();
  } catch (err) {
    alert('Falha ao adicionar livro. Veja console.'); console.error(err);
  }
});

async function deleteBook(id) {
  if (!confirm('Excluir livro ' + id + '?')) return;
  try {
    const res = await fetch(`${BOOKS_API}/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('erro');
    loadBooks();
  } catch (err) { alert('Falha ao excluir.'); console.error(err); }
}

async function editBookPrompt(id) {
  try {
    const res = await fetch(`${BOOKS_API}/${id}`);
    if (!res.ok) throw new Error('not found');
    const b = await res.json();
    const title = prompt('Título', b.title);
    if (title === null) return;
    const author = prompt('Autor', b.author || '');
    if (author === null) return;
    const copies = prompt('Cópias', b.copies || 1);
    if (copies === null) return;
    const payload = { title, author, copies: parseInt(copies,10) || 1 };
    const put = await fetch(`${BOOKS_API}/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (!put.ok) throw new Error('fail update');
    loadBooks();
  } catch (err) { alert('Falha ao editar.'); console.error(err); }
}

// initial load of books when page opens
window.addEventListener('load', () => loadBooks());
