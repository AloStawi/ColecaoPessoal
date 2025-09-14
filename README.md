# 📚 Coleção Pessoal de Livros

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Repositório destinado a aula Software Product: Analysis, Specification, Project & Implementation.<br>
Impacta Tecnologia


Um sistema simples em **Flask + MySQL** para gerenciar sua coleção pessoal de livros.  
Permite **cadastrar, listar, editar e excluir** livros, além de organizar por **gênero, status de leitura e notas**.  

---

## 🚀 Funcionalidades
- [x] **CRUD de livros** (adicionar, listar, editar, excluir)  
- [x] Status de leitura: *não lido, lendo, concluído*  
- [x] Avaliação pessoal (nota 0–10)  
- [x] Interface simples em HTML/CSS  

---

## 📂 Estrutura do Projeto
```
meu_projeto/
│
├── app.py               # Aplicação Flask
├── requirements.txt     # Dependências
├── static/              # Arquivos estáticos (CSS, imagens, JS)
│   └── style.css
└── templates/           # Páginas HTML (Jinja2)
    ├── base.html
    ├── index.html
    ├── add.html
    └── edit.html
```

---

## ⚙️ Como rodar o projeto

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/AloStawi/ColecaoPessoal.git
cd ColecaoPessoal
```

### 2️⃣ Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar credenciais no `app.py`
Edite estas linhas com seu usuário/senha do MySQL:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sua_senha'
app.config['MYSQL_DB'] = 'colecao_livros'
```

### 5️⃣ Rodar a aplicação
```bash
python app.py
```

