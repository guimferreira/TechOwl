from flask import Flask, render_template, request, redirect, session
import os
from unidecode import unidecode
import json

app = Flask(__name__)
app.secret_key = 'techowl'

os.environ["FLASK_DEBUG"] = "True"
app.debug = os.environ.get("FLASK_DEBUG") == "True"


def carregarGlossario():
    with open('dados.json', 'r', encoding='utf-8') as db:
        conceitos = json.load(db)
    return conceitos


def salvarGlossario(dicio):
    with open('dados.json', 'w', encoding='utf-8') as db:
        json.dump(dicio, db, ensure_ascii=False, indent=4)


def carregarTarefas(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as db:
        tarefas = [linha.strip() for linha in db.readlines()]
    return tarefas


def salvarTarefas(tarefas, arquivo):
    with open(arquivo, 'w', encoding='utf-8') as db:
        for tarefa in tarefas:
            db.write(tarefa + '\n')


conceitos = carregarGlossario()

listaDeTarefas = carregarTarefas('tarefas.txt')

prioridades = carregarTarefas('tarefaspriorizadas.txt')

selecionadas = carregarTarefas('tarefasfeitas.txt')


@app.route("/")
def index():
    
    return render_template("index.html")


@app.route("/glossario", methods=["GET", "POST"])
def glossario():
    if request.method == "POST":
        termo = request.form["termo"]
        definicao = request.form["definicao"]
        termo = termo.capitalize().rstrip()
        conceitos[termo] = definicao
        salvarGlossario(conceitos)
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


@app.route("/deletar/<string:termo>", methods=["GET", "POST"])
def deletarTermo(termo):
    del conceitos[termo]
    salvarGlossario(conceitos)
    return redirect("/glossario")


@app.route("/alterar-termo/<string:termo>", methods=["GET", "POST"])
def alterarTermo(termo):
    novoTermo = request.form["novotermo"]
    novoTermo = novoTermo.capitalize().rstrip()
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
    salvarGlossario(conceitos)
    return redirect("/glossario")


@app.route("/tarefas", methods=["GET", "POST"])
def tarefas():
    if request.method == "POST":
        tarefa = request.form['tarefa']
        if tarefa not in listaDeTarefas:
            listaDeTarefas.append(tarefa)
            salvarTarefas(listaDeTarefas, 'tarefas.txt')
        return redirect("/tarefas")
    else:
        return render_template("tarefas.html", listaDeTarefas=listaDeTarefas, prioridades=prioridades, selecionadas=selecionadas)


@app.route("/priorizar/<int:indice>")
def priorizar(indice):
    mover = listaDeTarefas.pop(indice)
    salvarTarefas(listaDeTarefas, 'tarefas.txt')
    prioridades.append(mover)
    salvarTarefas(prioridades, 'tarefaspriorizadas.txt')
    return redirect("/tarefas")


@app.route("/retirar-prioridade/<int:indice>")
def retirarPrioridade(indice):
    mover = prioridades.pop(indice)
    listaDeTarefas.append(mover)
    salvarTarefas(listaDeTarefas, 'tarefas.txt')
    salvarTarefas(prioridades, 'tarefaspriorizadas.txt')
    return redirect("/tarefas")


@app.route("/check/<int:indice>")
def checkbox(indice):
    tarefa = listaDeTarefas[indice]
    if tarefa in selecionadas:
        selecionadas.remove(tarefa)
    else:
        selecionadas.append(tarefa)
    salvarTarefas(selecionadas, 'tarefasfeitas.txt')
    return redirect("/tarefas")


@app.route("/check-up/<int:indice>")
def checkboxP(indice):
    tarefa = prioridades[indice]
    if tarefa in selecionadas:
        selecionadas.remove(tarefa)
    else:
        selecionadas.append(tarefa)
    salvarTarefas(selecionadas, 'tarefasfeitas.txt')
    return redirect("/tarefas")


@app.route("/del-tarefa/<int:indice>")
def deletarTarefa(indice):
    if listaDeTarefas[indice] in selecionadas:
        selecionadas.remove(listaDeTarefas[indice])
    del listaDeTarefas[indice]
    salvarTarefas(listaDeTarefas, 'tarefas.txt')
    salvarTarefas(selecionadas, 'tarefasfeitas.txt')
    return redirect("/tarefas")


@app.route("/del-up-tarefa/<int:indice>")
def deletarTarefaPriorizada(indice):
    if prioridades[indice] in selecionadas:
        selecionadas.remove(prioridades[indice])
    del prioridades[indice]
    salvarTarefas(prioridades, 'tarefaspriorizadas.txt')
    salvarTarefas(selecionadas, 'tarefasfeitas.txt')
    return redirect("/tarefas")


@app.route("/alterar-tarefa/<int:indice>", methods=["GET", "POST"])
def editarTarefa(indice):
    novaTarefa = request.form["novatarefa"]
    if listaDeTarefas[indice] in selecionadas:
        selecionadas.remove(listaDeTarefas[indice])
        selecionadas.append(novaTarefa)
    listaDeTarefas[indice] = novaTarefa
    salvarTarefas(listaDeTarefas, 'tarefas.txt')
    salvarTarefas(selecionadas, 'tarefasfeitas.txt')
    return redirect("/tarefas")


@app.route("/alterar-up-tarefa/<int:indice>", methods=["GET", "POST"])
def editarTarefaPriorizada(indice):
    novaTarefa = request.form["novatarefapriorizada"]
    if prioridades[indice] in selecionadas:
        selecionadas.remove(prioridades[indice])
        selecionadas.append(novaTarefa)
    prioridades[indice] = novaTarefa
    salvarTarefas(prioridades, 'tarefaspriorizadas.txt')
    salvarTarefas(selecionadas, 'tarefasfeitas.txt')
    return redirect("/tarefas")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


if __name__ == "__main__":
    app.run(debug=True)
