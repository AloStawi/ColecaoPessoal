from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import requests
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM livros")
    livros = cur.fetchall()
    cur.close()

    livros_com_capa = []
    for livro in livros:
        titulo = livro[1]
        autor = livro[2]

        # Busca na API pelo título e autor
        query = f"{titulo}+inauthor:{autor}"
        resposta = requests.get(GOOGLE_BOOKS_API, params={"q": query, "maxResults": 1})

        capa_url = ""
        if resposta.status_code == 200:
            dados = resposta.json()
            if "items" in dados:
                links = dados["items"][0]["volumeInfo"].get("imageLinks", {})
                capa_url = links.get("extraLarge") or links.get("large") or links.get("medium") or links.get("thumbnail") or ""

        livros_com_capa.append({
            "id": livro[0],
            "titulo": titulo,
            "autor": autor,
            "ano": livro[3],
            "genero": livro[4],
            "status": livro[5],
            "nota": livro[6],
            "capa": capa_url
        })

    return render_template("index.html", livros=livros_com_capa)

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    livros = []
    if request.method == "POST":
        termo = request.form["termo"]
        params = {"q": termo, "maxResults": 5, "printType": "books"}
        resposta = requests.get(GOOGLE_BOOKS_API, params=params)

        if resposta.status_code == 200:
            dados = resposta.json()
            for item in dados.get("items", []):
                info = item["volumeInfo"]
                livros.append({
                    "titulo": info.get("title", "Sem título"),
                    "autor": ", ".join(info.get("authors", ["Desconhecido"])),
                    "ano": info.get("publishedDate", "N/A")[:4],
                    "descricao": info.get("description", "Sem descrição"),
                    "capa": info.get("imageLinks", {}).get("thumbnail", "")
                })

    return render_template("buscar.html", livros=livros)

# Adicionar livro
@app.route('/addLivro', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']
        status = request.form['status_leitura']
        nota = request.form['nota']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO livros (titulo, autor, ano, genero, status_leitura, nota) VALUES (%s, %s, %s, %s, %s, %s)",
                    (titulo, autor, ano, genero, status, nota))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('addLivro.html')

# Editar livro
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']
        status = request.form['status_leitura']
        nota = request.form['nota']

        cur.execute("""
            UPDATE livros 
            SET titulo=%s, autor=%s, ano=%s, genero=%s, status_leitura=%s, nota=%s 
            WHERE id=%s
        """, (titulo, autor, ano, genero, status, nota, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM livros WHERE id=%s", (id,))
        livro = cur.fetchone()
        cur.close()
        return render_template('edit.html', livro=livro)

# Deletar livro
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM livros WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)