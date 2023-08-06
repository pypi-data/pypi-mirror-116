# pydenv
pydenv é um módulo criado para provisionar um ambiente de desenvolvimento,
com pacotes que promovem a estilização e documentação de código conforme a PEP8.

Além de provisionar corretamente o [pre-commit](https://pre-commit.com/) que será responsável por rodar todos os pacotes instalados antes de cada commit.

Criando assim códigos mais limpos, organizados e documentados.

## O quê acontece ao rodar o pydenv?
1. Instala o virtualenv
2. Cria um ambiente virtual
3. Instala os seguintes pacotes no ambiente virtual:
* Pylint
* Flake8
* Black
* Mypy
* Pydocstyle
* Pytest
* Pre-Commit
4. Cria os arquivos de configuração dos pacotes informados a cima.
5. Cria a estrutura de projeto com src, main, test, build
6. Roda o Pre-Commit

## Utilizando
O pydenv pode ser usado da seguinte maneira

````
1. pip install pydenv
2. git clone <CloneRepo>
3. cd <DirRepo>
4. python3 -m pydenv
````