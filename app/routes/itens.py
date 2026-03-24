from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import CatalogoItem

bp = Blueprint('itens', __name__)

@bp.route('/')
def listar_itens():
    itens = CatalogoItem.query.all()
    return render_template('itens_list.html', itens=itens)

@bp.route('/novo', methods=['GET', 'POST'])
def novo_item():
    if request.method == 'POST':
        descricao = request.form.get('descricao_completa')
        
        item = CatalogoItem(descricao_completa=descricao)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('itens.listar_itens'))
    
    return render_template('item_form.html')
