from flask import Flask, render_template, request, redirect
import os
from unidecode import unidecode # ignorar ignorar acentuação e caracteres especiais

app = Flask(__name__)

os.environ["FLASK_DEBUG"] = "True"
app.debug = os.environ.get("FLASK_DEBUG") == "True"


definicoes = {
    "Algoritmo": "Conjunto de regras e procedimentos lógicos perfeitamente definidos que levam à solução de um problema em um número finito de etapas.",
    "Pseudocódigo": "Organiza o algoritmo numa linguagem natural seguindo uma lógica computacional.",
    "Dado": "Matéria-prima da computação, pode ser manipulado e/ou armazenado.",
    "Função": "Uma série de instruções que retorna algum valor para um chamador. Também pode ser passado zero ou mais argumentos que podem ser usados na execução do corpo.",
    "Método": "Uma função que é definida dentro do corpo de uma classe. Se chamada como um atributo de uma instância daquela classe, o método receberá a instância do objeto como seu primeiro argumento (que comumente é chamado de self).",
    "Ambiente virtual": "Um ambiente de execução isolado que permite usuários e aplicações instalarem e atualizarem pacotes Python sem interferir no comportamento de outras aplicações Python em execução no mesmo sistema.",
}

listaDeTarefas = []

prioridades = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/glossario", methods=["GET", "POST"])
def glossario():
    if request.method == "POST":
        termo = request.form["termo"]
        definicao = request.form["definicao"]
        termo = termo.capitalize()
        definicoes[termo] = definicao
        return redirect("/glossario")
    else:
        pesquisa = request.args.get("pesquisar", "").lower()
        pesquisa = unidecode(pesquisa)
        if pesquisa:
            pesquisado = {
                termo: descricao
                for termo, descricao in definicoes.items()
                if pesquisa in unidecode(termo.lower())
            }
        else:
            pesquisado = definicoes
    return render_template("glossario.html", glossario=sorted(definicoes.items()), pesquisado=pesquisado, pesquisa=pesquisa)


@app.route("/deletar/<string:termo>")
def deletarTermo(termo):
    definicoes.pop(termo)
    return redirect("/glossario")


@app.route("/alterar-termo/<string:termo>", methods=["GET", "POST"])
def alterarTermo(termo):
    novoTermo = request.form["novotermo"]
    novaDefinicao = request.form["novadefinicao"]
    if novoTermo == "" and novaDefinicao == "":
        return redirect("/glossario")
    elif novoTermo == "":
        definicoes[termo] = novaDefinicao
    elif novaDefinicao == "":
        definicoes.setdefault(novoTermo, definicoes.pop(termo))
    else:
        definicoes.setdefault(novoTermo, definicoes.pop(termo))
        definicoes[novoTermo] = novaDefinicao
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
