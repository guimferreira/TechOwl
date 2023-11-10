from flask import Flask, render_template, request, redirect
import os

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

listadetarefas = []

prioridades = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/glossario", methods=["GET", "POST"])
def glossario():
    if request.method == "POST":
        termo = request.form["termo"]
        definicao = request.form["definicao"]
        definicoes[termo] = definicao
        return redirect("/glossario")
    else:
        return render_template(
            "glossario.html",
            glossario=sorted(definicoes.items(), key=lambda x: x[0].lower()),
        )


@app.route("/deletar/<string:termo>")
def deletartermo(termo):
    definicoes.pop(termo)
    return redirect("/glossario")


@app.route("/alterar/<string:termo>", methods=["GET", "POST"])
def alterartermo(termo):
    novotermo = request.form["novotermo"]
    novadefinicao = request.form["novadefinicao"]
    if novotermo == "" and novadefinicao == "":
        return redirect("/glossario")
    elif novotermo == "":
        definicoes[termo] = novadefinicao
    elif novadefinicao == "":
        definicoes.setdefault(novotermo, definicoes.pop(termo))
    else:
        definicoes.setdefault(novotermo, definicoes.pop(termo))
        definicoes[novotermo] = novadefinicao
    return redirect("/glossario")


@app.route("/tarefas", methods=["GET", "POST"])
def tarefas():
    if request.method == "POST":
        tarefa = request.form['tarefa']
        listadetarefas.append(tarefa)
        return redirect("/tarefas")
    else:
        return render_template("tarefas.html", listadetarefas=listadetarefas, prioridades=prioridades)


@app.route("/priorizar/<int:indice>")
def priorizar(indice):
    mover = listadetarefas.pop(indice)
    prioridades.append(mover)
    return redirect("/tarefas")


@app.route("/del-tarefa/<int:indice>")
def delTarefa(indice):
    listadetarefas.pop(indice)
    return redirect("/tarefas")


@app.route("/del-up-tarefa/<int:indice>")
def deletartarefa(indice):
    prioridades.pop(indice)
    return redirect("/tarefas")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


if __name__ == "__main__":
    app.run(debug=True)
