# !/usr/bin/python3
# encoding: ISO-8859-1
"""
Módulo criado para realizar o processo de criação de ambiente de desenvolvimento."""
import sys


def run_pydenv():
    from pydenv.pydenv import run as PydenvRun
    try:
        PydenvRun()
    except KeyboardInterrupt:
        sys.exit(1)