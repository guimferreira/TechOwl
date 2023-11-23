from flask import Flask, render_template, request, redirect
import os
from unidecode import unidecode
import json

app = Flask(__name__)

os.environ["FLASK_DEBUG"] = "True"
app.debug = os.environ.get("FLASK_DEBUG") == "True"


def carregar():
    with open('dados.json', 'r', encoding='utf-8') as db:
        conceitos = json.load(db)
    return conceitos



def salvar(conceitos):
    with open('dados.json', 'w', encoding='utf-8') as db:
        json.dump(conceitos, db, ensure_ascii=False, indent=4)


listaDeTarefas = []

prioridades = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/glossario", methods=["GET", "POST"])
def glossario():

    conceitos = carregar()
    if request.method == "POST":
        termo = request.form["termo"]
        definicao = request.form["definicao"]
        termo = termo.capitalize().rstrip()
        conceitos[termo] = definicao
        salvar(conceitos)
        return redirect("/glossario")
    else:
        pesquisa = request.args.get("pesquisar", "").lower()
        pesquisa = unidecode(pesquisa)
        if pesquisa:
            pesquisado = {
                termo: descricao
                for termo, descricao in conceitos.items()
                if pesquisa in unidecode(termo.lower())
            }
        else:
            pesquisado = conceitos

    return render_template("glossario.html", glossario=sorted(conceitos.items()), pesquisado=pesquisado, pesquisa=pesquisa)


@app.route("/deletar/<string:termo>")
def deletarTermo(termo):
    conceitos = carregar()
    del conceitos[termo]
    salvar(conceitos)
    return redirect("/glossario")


@app.route("/alterar-termo/<string:termo>", methods=["GET", "POST"])
def alterarTermo(termo):
    conceitos = carregar()
    novoTermo = request.form["novotermo"]
    novaDefinicao = request.form["novadefinicao"]
    if novoTermo == "" and novaDefinicao == "":
        return redirect("/glossario")
    elif novoTermo == "":
        conceitos[termo] = novaDefinicao
    elif novaDefinicao == "":
        conceitos.setdefault(novoTermo, conceitos.pop(termo))
    else:
        conceitos.setdefault(novoTermo, conceitos.pop(termo))
        conceitos[novoTermo] = novaDefinicao
    salvar(conceitos)
    return redirect("/glossario")


@app.route("/tarefas", methods=["GET", "POST"])
def tarefas():
    if request.method == "POST":
        tarefa = request.form['tarefa']
        listaDeTarefas.append(tarefa)
        return redirect("/tarefas")
    else:
        return render_template("tarefas.html", listaDeTarefas=listaDeTarefas, prioridades=prioridades)


@app.route("/priorizar/<int:indice>")
def priorizar(indice):
    mover = listaDeTarefas.pop(indice)
    prioridades.append(mover)
    return redirect("/tarefas")


@app.route("/retirar-prioridade/<int:indice>")
def retirarPrioridade(indice):
    mover = prioridades.pop(indice)
    listaDeTarefas.append(mover)
    return redirect("/tarefas")


@app.route("/del-tarefa/<int:indice>")
def deletarTarefa(indice):
    listaDeTarefas.pop(indice)
    return redirect("/tarefas")


@app.route("/del-up-tarefa/<int:indice>")
def deletarTarefaPriorizada(indice):
    del prioridades[indice]
    return redirect("/tarefas")


@app.route("/alterar-tarefa/<int:indice>", methods=["GET", "POST"])
def editarTarefa(indice):
    novaTarefa = request.form["novatarefa"]
    listaDeTarefas[indice] = novaTarefa
    return redirect("/tarefas")


@app.route("/alterar-up-tarefa/<int:indice>", methods=["GET", "POST"])
def editarTarefaPriorizada(indice):
    novaTarefa = request.form["novatarefapriorizada"]
    prioridades[indice] = novaTarefa
    return redirect("/tarefas")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


if __name__ == "__main__":
    app.run(debug=True)
