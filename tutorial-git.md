arquivo para testar a criação de uma branch

links úteis:

Criar e deletar uma branch:
https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository

Sobre Branches:
https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches

Sobre pull requests:
https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests

Criar um pull request:
https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request?tool=desktop

Sobre conflitos de merge:
https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts

No terminal `$` significa a linha do terminal em caso de duvidas:

```
$ git --help
```

Pra trocar de branch:

```
$ git checkout 'nome da branch'
```

Pra criar um novo branch:

```
$ git checkout -b 'nome da branch'
```

Pra adicionar arquivos que vão ser commitados:

```
$ git add <arquivo>
$ git add .             # adiciona todos os arquivos da pasta atual
                        # e das pastas dentro dela
```

Status do commit ou da área de staging:

```
$ git status
```

Criar um commit:

```
$ git commit -m <mensagem>
```

Subir o commit em um branch novo pela primeira vez:

```
$ git push -u origin <nome do seu branch>
$ git push --set-upstream origin <nome do seu branch>
# -u é a mesma coisa que --set-upstream
```

_O `-u` configura o seu branch local pra estar alinhado com o branch de mesmo nome no repositório remoto_

Daí em diante, não vai mais precisar do `-u origin <nome do seu branch>`:

```
$ git push
```

Pra baixar as mudanças:

```
$ git pull
```

No github:

- Abrir a branch criada
- vai ter a seguinte mensagem:
  "This branch is 1 commit ahead main."
- ao lado tem a opção "contribute", nela você pode criar o pull request
- quando eu estiver viajando, vocês podem fazer o merge na main se quiserem:
  - abrir a aba de pull request
  - se não tiver conflitos, clicar em "merge pull request"
  - se tiver conflitos, ver a documentação do github sobre conflitos
