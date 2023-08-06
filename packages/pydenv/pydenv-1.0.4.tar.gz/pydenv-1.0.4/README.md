# pydenv
pydeenv é um módulo criado para provisionar um ambiente de desenvolvimento.
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

# Usando
O pydenv pode ser usado da seguinte maneira
````
1. pip install pydenv
2. git clone <CloneRepo>
3. python3 -m pydenv
````
