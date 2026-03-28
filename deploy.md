# Guia de Deploy (Supabase + Render + PythonAnywhere)

Este documento descreve os passos necessários para configurar o banco de dados PostgreSQL no **Supabase** e realizar o deploy da aplicação no **Render** e **PythonAnywhere**.

---

## 1. Configurando o Supabase (Banco de Dados)

### Passo a Passo:
1.  Acesse [supabase.com](https://supabase.com/) e faça login.
2.  Clique em **"New Project"** e escolha sua organização.
3.  Preencha os dados:
    -   **Name**: `app_prescricao` (ou o nome que desejar).
    -   **Database Password**: Escolha uma senha forte e **guarde-a**.
    -   **Region**: Escolha uma região próxima (ex: `São Paulo - sa-east-1`).
4.  Clique em **"Create new project"**. Aguarde alguns minutos até que o banco de dados seja provisionado.

### Obtendo a String de Conexão:
1.  No painel lateral, clique em **Project Settings** (ícone de engrenagem).
2.  Vá em **Database**.
3.  Role para baixo até encontrar a seção **Connection string**.
4.  Selecione a aba **URI**.
5.  A string de conexão será algo como: 
    `postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres`
6.  Substitua `[YOUR-PASSWORD]` pela senha que você criou. **Esta é a sua `DATABASE_URL`.**

---

## 2. Configurando o Render (Servidor Web)

### Passo a Passo:
1.  Acesse [render.com](https://render.com/) e faça login (recomenda-se conectar com o GitHub).
2.  Clique em **"New +"** e selecione **"Web Service"**.
3.  Conecte seu repositório do GitHub onde o código está hospedado.
4.  Configure os campos fundamentais:
    -   **Name**: `app-prescricao`
    -   **Runtime**: `Python 3`
    -   **Build Command**: `./build.sh`
    -   **Start Command**: `gunicorn run:app`
5.  Clique em **"Advanced"** para configurar as **Environment Variables**.

---

## 3. Variáveis de Ambiente (Configurações Cruciais)

No painel do Render (aba **Environment**), adicione as seguintes chaves:

| Chave | Valor |
| :--- | :--- |
| `DATABASE_URL` | A URI que você copiou do Supabase. |
| `SECRET_KEY` | Uma string aleatória e segura (ex: `minha_chave_secreta_123`). |
| `FLASK_APP` | `run.py` |
| `PYTHON_VERSION` | `3.10.0` (opcional, ou a versão que preferir). |

---

## 4. O Script de Build (`build.sh`)

O arquivo `build.sh` no repositório já está configurado para:
1.  Instalar as dependências (`pip install`).
2.  Executar as migrações do banco de dados (`flask db upgrade`).
3.  Popular o catálogo inicial (`python seed_catalogo.py`).

Isso garante que, toda vez que você fizer um deploy ou atualização, o banco de dados do Supabase será atualizado automaticamente com a estrutura correta.

---

## 5. Configurando o PythonAnywhere

> [!IMPORTANT]
> **Atenção**: Para conectar o PythonAnywhere ao Supabase, você precisa ter uma conta paga (**Hacker plan** ou superior), pois contas gratuitas não permitem conexões de saída para bancos de dados externos.

### Passo a Passo:
1.  No PythonAnywhere, vá para a aba **Web**.
2.  Clique em **"Add a new web app"**.
3.  Selecione **Manual Configuration** e escolha o **Python 3.10** (ou a versão desejada).
4.  No terminal do PythonAnywhere, clone o seu repositório:
    `git clone https://github.com/seu-usuario/app_prescricao.git`
5.  Crie um ambiente virtual e instale as dependências:
    ```bash
    mkvirtualenv --python=/usr/bin/python3.10 venv_prescricao
    pip install -r requirements.txt
    ```
6.  **Configurando o WSGI File**:
    -   Na aba Web, localize o link **WSGI configuration file**.
    -   Edite o arquivo e aponte para a sua aplicação:
        ```python
        import os
        import sys

        path = '/home/seu-usuario/app_prescricao'
        if path not in sys.path:
            sys.path.append(path)

        os.environ['DATABASE_URL'] = 'sua-url-do-supabase-aqui'
        os.environ['SECRET_KEY'] = 'sua-secret-key'

        from wsgi import app as application
        ```
7.  **Variáveis de Ambiente**: Diferente do Render, no PythonAnywhere o ideal é colocar as variáveis `DATABASE_URL` e `SECRET_KEY` diretamente no arquivo WSGI (como mostrado acima) ou usar um arquivo `.env`.

---

## 6. Dicas Importantes

-   **Certificados SSL**: O Render e o Supabase usam conexões seguras por padrão. A configuração do SQLAlchemy no `config.py` já está preparada para lidar com isso.
-   **Logs**: Você pode acompanhar o progresso das migrações e do boot da aplicação na aba **"Logs"** do Render.
-   **Static Files**: Como é uma aplicação Flask, as imagens e arquivos CSS em `app/static/` serão servidos automaticamente. Para PDFs gerados, eles são mantidos temporariamente no sistema de arquivos do Render (atenção: o Render tem sistema de arquivos efêmero se não usar persistent disk).
