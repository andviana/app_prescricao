from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Configuracao

bp = Blueprint('configuracoes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def configurar():
    config = Configuracao.query.first()
    if not config:
        config = Configuracao()
        db.session.add(config)
        db.session.commit()
    
    if request.method == 'POST':
        config.nome_empresa = request.form.get('nome_empresa', '').strip()
        config.telefone = request.form.get('telefone', '').strip()
        config.email = request.form.get('email', '').strip()
        
        if not config.nome_empresa:
            flash('O Nome da Empresa não pode ficar em branco.')
        else:
            db.session.commit()
            flash('Configurações salvas com sucesso!')
            return redirect(url_for('configuracoes.configurar'))
            
    return render_template('configuracoes.html', config=config)
