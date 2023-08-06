# !/usr/bin/python3
# encoding: ISO-8859-1
"""M�dulo criado para realizar o processo de cria��o de ambiente de desenvolvimento."""

import os
import sys
import subprocess
import logging

LISTA_PKGS = ["flake8", "pylint", "black", "mypy", "pydocstyle", "pytest", "pre-commit"]


def extrai_caminho_projeto(*args: str) -> str:
    """
    Coleta o caminho para realizar os processos de cria��o do ambiente.

    Parameter
    Return
        :return: Caminho e Nome do projeto
        :rtype: str, str

    Exemple
        >>> path = "/home/dev/DevProjects/pydenv/"
        >>> extrai_caminho_projeto(path)
        "/home/dev/DevProjects"

    """
    if args is not None:
        caminho_projeto: str = os.getcwd()
        return caminho_projeto


def extrai_nome_projeto(*args: str) -> str:
    """
    Coleta o nome do projeto com base os.path.

    Parameter
        :param args: Caminho do projeto
        :type args: str

    Return
        :return: Nome Projeto
        :rtype: str

    Exemple
        >>> path = "/home/dev/DevProjects/pydenv/"
        >>> extrai_nome_projeto(path)
        "pydenv"

    """
    if args is not None:
        nome_projeto: str = os.path.basename(extrai_caminho_projeto())
        return nome_projeto


def instala_pkgs_pip(pkg: str) -> bool:
    """
    Realiza a instala��o do pacote com nome passado no argumento

    Parameter
        :param pkg: Nome do pacote pip
        :type pkg: str
    Return

    Exemple
        >>> instala_pkgs_pip('virtualenv')
        True

    """
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
        return True
    except KeyboardInterrupt:
        return False


def install_virtualenv() -> bool:
    """
    Realiza a instala��o do pacote virtualenv

    Parameter

    Return

    Exemple
        >>> install_virtualenv()
        True
    """
    try:
        instala_pkgs_pip('virtualenv')
        return True
    except KeyboardInterrupt:
        return False


def cria_virtual_env(nome_projeto: str = extrai_nome_projeto()) -> bool:
    """
    Cria o ambiente virtual com base no nome do projeto

    Parameter

    Return

    Exemple
        >>> cria_virtual_env()
        True

    """
    try:
        os.system(f'virtualenv .venv --prompt "({nome_projeto}) "')
        return True
    except KeyboardInterrupt:
        return False


def activate_virtual_env_and_install_pkg_pip() -> bool:
    """
    Ativa o ambiente virtual e instala os pacotes PIP necess�rios.

    Parameter

    Return

    """
    try:
        os.system(f'. .venv/bin/activate &&'
                  f'pip install flake8 &&'
                  f'pip install pylint &&'
                  f'pip install black &&'
                  f'pip install mypy &&'
                  f'pip install pydocstyle &&'
                  f'pip install pytest &&'
                  f'pip install pre-commit')
        return True
    except KeyboardInterrupt:
        return False


def donwload_files_config() -> bool:
    """
    Realiza o donwload dos arquivos de configura��o padr�o

    Parameter

    Return

    Example
        >>> donwload_files_config()
        True

    """
    try:

        os.system(
            'wget https://raw.githubusercontent.com/felipe-almeida-costa-leite/pydenv/main/pydenv/config_files'
            '/.flake8')
        os.system(
            'wget https://raw.githubusercontent.com/felipe-almeida-costa-leite/pydenv/main/pydenv/config_files'
            '/.pydocstyle.ini')
        os.system(
            'wget https://raw.githubusercontent.com/felipe-almeida-costa-leite/pydenv/main/pydenv/config_files'
            '/.pylintrc')
        os.system(
            'wget https://raw.githubusercontent.com/felipe-almeida-costa-leite/pydenv/main/pydenv/config_files'
            '/conftest.py')
        os.system(
            'wget https://raw.githubusercontent.com/felipe-almeida-costa-leite/pydenv/main/pydenv/config_files/mypy'
            '.ini')
        os.system(
            'wget wget https://raw.githubusercontent.com/felipe-almeida-costa-leite/pydenv/main/pydenv/config_files'
            '/.pre-commit-config.yaml')
        return True
    except KeyboardInterrupt:
        return False


def install_pre_commit() -> bool:
    """
    Realizar a instala��o do pre-commit

    Parameter

    Return

    Example
        >>> install_pre_commit()
        True
    """
    try:
        os.system('. .venv/bin/activate && pre-commit install')
        return True
    except KeyboardInterrupt:
        return False


def cria_estrutura_diretorios() -> bool:
    """
    Cria a Estrutura de diret�rios necess�ria

    Parameter

    Return

    Example
        >>> cria_estrutura_diretorios()
    """
    try:
        os.system('mkdir src && mkdir build && cd src && mkdir main && mkdir test')
        return True
    except KeyboardInterrupt:
        return False


def run():
    """
    Fun��o que realiza o processo de provisionamento do ambiente

    Parameter

    Return

    Example
        >>> run()
        True

    """

    logging.info('Iniciando processo de configura��o do reposit�rio.')
    logging.info('Extraindo nome do projeto.')
    nome = extrai_nome_projeto()
    logging.info('Checando a instala��o do virtualenv.')
    install_virtualenv()
    logging.info('Cria��o do ambiente virtual.')
    cria_virtual_env(nome)
    logging.info('Ativa��o do ambiente virtual.')
    activate_virtual_env_and_install_pkg_pip()
    logging.info('Baixando os arquivos padr�o.')
    donwload_files_config()
    logging.info('Configurando o pre-commit.')
    install_pre_commit()
    logging.info('Criando a estrutura de diret�rios')
    cria_estrutura_diretorios()
    logging.info('Processo finalizado, bom desenvolvimento!')
