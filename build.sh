#!/usr/bin/env bash
# Saia em caso de erro
set -o errexit

# Instala as dependências
pip install -r requirements.txt

# Executa as migrações do banco de dados (Cria as tabelas no PostgreSQL ou SQLite)
flask db upgrade

# Popula o banco com os dados iniciais do catálogo (ignora os que já existem)
python seed_catalogo.py
