document.addEventListener("DOMContentLoaded", () => {
  console.log("Dashboard da Biblioteca carregado 🎉");
});

const books = [
  {
    titulo: "1984",
    autor: "George Orwell",
    genero: "Distopia",
    capa: "https://covers.openlibrary.org/b/id/153541-L.jpg",
    status: "concluído"
  },
  {
    titulo: "Dom Casmurro",
    autor: "Machado de Assis",
    genero: "Clássico",
    capa: "https://covers.openlibrary.org/b/id/8231991-L.jpg",
    status: "lendo"
  },
  {
    titulo: "O Hobbit",
    autor: "J.R.R. Tolkien",
    genero: "Fantasia",
    capa: "https://covers.openlibrary.org/b/id/6979861-L.jpg",
    status: "não lido"
  },
  {
    titulo: "A Revolução dos Bichos",
    autor: "George Orwell",
    genero: "Sátira",
    capa: "https://covers.openlibrary.org/b/id/240726-L.jpg",
    status: "lendo"
  }
];

// Renderiza os livros
function renderBooks(lista) {
  const container = document.getElementById("bookList");
  container.innerHTML = "";

  lista.forEach(livro => {
    const card = document.createElement("div");
    card.classList.add("book-card");

    card.innerHTML = `
      <div class="book-cover">
        <img src="${livro.capa}" alt="${livro.titulo}">
      </div>
      <div class="book-info">
        <h3>${livro.titulo}</h3>
        <p>${livro.autor}</p>
        <span class="status">${livro.status}</span>
      </div>
    `;

    container.appendChild(card);
  });
}

// Filtro por status
const buttons = document.querySelectorAll(".filter-btn");
buttons.forEach(btn => {
  btn.addEventListener("click", () => {
    buttons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    const filtro = btn.getAttribute("data-filter");
    if (filtro === "all") renderBooks(books);
    else renderBooks(books.filter(l => l.status === filtro));
  });
});

// Busca
const searchInput = document.getElementById("searchInput");
searchInput.addEventListener("input", e => {
  const valor = e.target.value.toLowerCase();
  const filtrados = books.filter(l =>
    l.titulo.toLowerCase().includes(valor) ||
    l.autor.toLowerCase().includes(valor) ||
    l.genero.toLowerCase().includes(valor)
  );
  renderBooks(filtrados);
});

renderBooks(books);


document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const bookList = document.getElementById('bookList');
    const bookCards = bookList.querySelectorAll('.book-card');

    let currentFilter = 'all';
    let currentSearchTerm = '';

    // Função principal para aplicar filtros e busca
    const applyFilters = () => {
        bookCards.forEach(card => {
            const status = card.getAttribute('data-status');
            // Busca nos atributos em minúsculo definidos no HTML
            const title = card.getAttribute('data-title');
            const author = card.getAttribute('data-author');
            const genre = card.getAttribute('data-genre');
            
            // 1. Verificar Filtro de Status
            const isFiltered = currentFilter === 'all' || status === currentFilter;

            // 2. Verificar Busca por Texto (Busca em Título, Autor ou Gênero)
            const matchesSearch = title.includes(currentSearchTerm) ||
                                  author.includes(currentSearchTerm) ||
                                  genre.includes(currentSearchTerm);

            // 3. Exibir ou Esconder
            if (isFiltered && matchesSearch) {
                card.style.display = 'flex'; // Exibe o card (ajustado para flex no CSS)
            } else {
                card.style.display = 'none';
            }
        });
    };

    // Evento para a Busca (Search Input)
    searchInput.addEventListener('input', (e) => {
        // Converte para minúsculas e remove espaços extras
        currentSearchTerm = e.target.value.trim().toLowerCase();
        applyFilters();
    });

    // Evento para os Botões de Filtro
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // 1. Atualiza o filtro ativo visualmente
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // 2. Define o novo filtro
            currentFilter = button.getAttribute('data-filter');
            applyFilters();
        });
    });

    // Aplica os filtros ao carregar a página
    applyFilters();
});