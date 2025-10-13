from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL, MySQLdb
import requests
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

@app.route('/')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, titulo, autor, ano, genero, status_leitura, nota, paginas_totais, paginas_lidas 
        FROM livros
    """)
    livros_db = cur.fetchall()
    cur.close()

    livros_processados = []
    total_paginas_lidas = 0

    concluidos_mes = 0 
    paginas_mes = 0

    for livro in livros_db:
        status = livro[5].lower() 
        paginas_totais = livro[7] or 1
        paginas_lidas_do_livro = livro[8] if livro[8] is not None else 0 # Trata valor nulo

        dados_livro = {
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "ano": livro[3],
            "genero": livro[4],
            "status": status,
            "nota": livro[6],
            "paginas_total": paginas_totais,
            "paginas_lidas": paginas_lidas_do_livro,
            "capa": "" # Inicializa sem capa
        }

        if status == "lendo":
            query = f"{dados_livro['titulo']}+inauthor:{dados_livro['autor']}"
            try:
                resposta = requests.get(GOOGLE_BOOKS_API, params={"q": query, "maxResults": 1}, timeout=5)
                if resposta.status_code == 200:
                    dados = resposta.json()
                    if "items" in dados:
                        links = dados["items"][0]["volumeInfo"].get("imageLinks", {})
                        dados_livro["capa"] = (
                            links.get("extraLarge") or
                            links.get("large") or
                            links.get("medium") or
                            links.get("thumbnail") or
                            ""
                        )
            except requests.exceptions.RequestException:
                dados_livro["capa"] = ""
        

        livros_processados.append(dados_livro)

        if status == "concluído":
            total_paginas_lidas += dados_livro["paginas_total"]
            concluidos_mes += 1
            paginas_mes += dados_livro["paginas_total"]

        elif status == "lendo":
            total_paginas_lidas += dados_livro["paginas_lidas"]
            paginas_mes += dados_livro["paginas_lidas"] # Corrigido de 'pagnias_mes' para 'paginas_mes'

    total_livros = len(livros_processados)
    concluidos = len([l for l in livros_processados if l['status'] == 'concluído'])
    lendo = len([l for l in livros_processados if l['status'] == 'lendo'])
    lendo_atualmente = [l for l in livros_processados if l['status'] == 'lendo'][:3]

    return render_template(
        "dashboard.html",
        livros_processados=livros_processados,
        lendo_atualmente=lendo_atualmente,
        total_livros=total_livros,
        concluidos=concluidos,
        lendo=lendo,
        paginas_lidas=int(total_paginas_lidas),
        concluidos_mes=concluidos_mes,
        paginas_mes=int(paginas_mes) 
    )

@app.route('/biblioteca')
def biblioteca():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, titulo, autor, ano, genero, status_leitura, nota, paginas_totais, paginas_lidas
        FROM livros
    """)
    livros_db = cur.fetchall()
    cur.close()

    livros_com_capa = []
    for livro in livros_db:
        titulo, autor, status = livro[1], livro[2], livro[5].lower()
        paginas_totais = livro[7] or 1
        paginas_lidas_do_livro = livro[8] if livro[8] is not None else 0
        query = f"{titulo}+inauthor:{autor}"
        capa_url = ""

        try:
            resposta = requests.get(GOOGLE_BOOKS_API, params={"q": query, "maxResults": 1}, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                if "items" in dados:
                    links = dados["items"][0]["volumeInfo"].get("imageLinks", {})
                    capa_url = (
                        links.get("extraLarge") or
                        links.get("large") or
                        links.get("medium") or
                        links.get("thumbnail") or
                        ""
                    )
        except requests.exceptions.RequestException:
            capa_url = ""

        livros_com_capa.append({
            "id": livro[0],
            "titulo": titulo,
            "autor": autor,
            "ano": livro[3],
            "genero": livro[4],
            "status": status,
            "nota": livro[6],
            "paginas_total": paginas_totais,
            "paginas_lidas": paginas_lidas_do_livro,
            "capa": capa_url
        })

    return render_template("biblioteca.html", livros=livros_com_capa)

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    livros = []
    if request.method == "POST":
        termo = request.form["termo"]
        params = {"q": termo, "maxResults": 5, "printType": "books"}
        try:
            resposta = requests.get(GOOGLE_BOOKS_API, params=params, timeout=5)
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
        except requests.exceptions.RequestException:
            pass

    return render_template("buscar.html", livros=livros)

@app.route('/livros/novo', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']
        status_leitura = request.form['status_leitura']
        nota = request.form['nota']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO livros (titulo, autor, ano, genero, status_leitura, nota)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (titulo, autor, ano, genero, status_leitura, nota))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('biblioteca'))

    return render_template('addLivro.html')

@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']
        status_leitura = request.form['status_leitura']
        nota = request.form['nota']
        descricao = request.form['descricao']
        paginas_totais = request.form.get('paginas_totais', None)
        paginas_lidas = request.form['paginas_lidas']

        cur.execute("""
            UPDATE livros 
            SET titulo=%s, autor=%s, ano=%s, genero=%s, status_leitura=%s, nota=%s, descricao=%s, paginas_totais=%s, paginas_lidas=%s
            WHERE id=%s
        """, (titulo, autor, ano, genero, status_leitura, nota, descricao, paginas_totais, paginas_lidas, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('biblioteca'))
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM livros WHERE id = %s", (id,))
        livro = cur.fetchone()
        cur.close()
        return render_template('edit.html', livro=livro)

@app.route('/livros/deletar/<int:id>')
def deletar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM livros WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('biblioteca'))

if __name__ == "__main__":
    app.run(debug=True)
