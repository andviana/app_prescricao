from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from app import db
from app.models import Internacao, Prescricao, PrescricaoItens, CatalogoItem
from datetime import datetime
from app.services.pdf_service import gerar_pdf_prescricao

bp = Blueprint('prescricoes', __name__)

@bp.route('/<int:internacao_id>/nova', methods=['GET', 'POST'])
def nova_prescricao(internacao_id):
    internacao = db.session.get(Internacao, internacao_id)
    if not internacao:
        flash('Internação não encontrada.')
        return redirect(url_for('main.dashboard'))
    # Lógica de "Cópia do Dia": Carregar itens da última prescrição
    ultima_prescricao = Prescricao.query.filter_by(internacao_id=internacao_id).order_by(Prescricao.data_prescricao.desc(), Prescricao.version_number.desc()).first()
    
    itens_pre_selecionados = []
    if ultima_prescricao:
        itens_pre_selecionados = [item.descricao_foto for item in ultima_prescricao.itens]

    if request.method == 'POST':
        # Captura itens marcados
        itens_ids = request.form.getlist('itens')
        data_presc_str = request.form.get('data_prescricao')
        data_presc = datetime.strptime(data_presc_str, '%Y-%m-%d').date() if data_presc_str else internacao.data_internacao
        
        # Verificar versão
        mesma_data = Prescricao.query.filter_by(internacao_id=internacao_id, data_prescricao=data_presc).order_by(Prescricao.version_number.desc()).first()
        nova_versao = mesma_data.version_number + 1 if mesma_data else 1
        
        nova_presc = Prescricao(
            internacao_id=internacao_id,
            data_prescricao=data_presc,
            version_number=nova_versao
        )
        db.session.add(nova_presc)
        db.session.flush() # Para pegar o ID
        for i_desc in itens_ids:
            p_item = PrescricaoItens(
                prescricao_id=nova_presc.id,
                descricao_foto=i_desc
            )
            db.session.add(p_item)
                
        db.session.commit()
        flash('Prescrição gerada com sucesso!')
        return redirect(url_for('prescricoes.visualizar_pdf', prescricao_id=nova_presc.id))

    return render_template('prescricao_form.html', internacao=internacao, itens_pre_selecionados=itens_pre_selecionados)

@bp.route('/api/catalogo')
def api_catalogo():
    q = request.args.get('q', '')
    query = CatalogoItem.query
    if q:
        query = query.filter(CatalogoItem.descricao_completa.ilike(f'%{q}%'))
    itens = query.order_by(CatalogoItem.descricao_completa.asc()).all()
    return jsonify([{'descricao': item.descricao_completa} for item in itens])

@bp.route('/<int:prescricao_id>/pdf')
def visualizar_pdf(prescricao_id):
    prescricao = db.session.get(Prescricao, prescricao_id)
    if not prescricao:
        flash('Prescrição não encontrada.')
        return redirect(url_for('main.dashboard'))
        
    pdf_path = gerar_pdf_prescricao(prescricao)
    return send_file(pdf_path, as_attachment=False, mimetype='application/pdf')

@bp.route('/<int:internacao_id>/lista')
def listar_prescricoes(internacao_id):
    internacao = db.session.get(Internacao, internacao_id)
    if not internacao:
        flash('Internação não encontrada.')
        return redirect(url_for('main.dashboard'))
    
    prescricoes = Prescricao.query.filter_by(internacao_id=internacao_id).order_by(Prescricao.data_prescricao.desc(), Prescricao.version_number.desc()).all()
    
    return render_template('prescricoes_list.html', internacao=internacao, prescricoes=prescricoes)
