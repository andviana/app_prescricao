from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Internacao, Paciente
from datetime import datetime

bp = Blueprint('internacoes', __name__)

@bp.route('/novo', methods=['GET', 'POST'])
def nova_internacao():
    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        data_int_str = request.form.get('data_internacao')
        hipotese = request.form.get('hipotese_diagnostica')

        data_internacao = datetime.strptime(data_int_str, '%Y-%m-%d').date() if data_int_str else datetime.today().date()

        internacao = Internacao(
            paciente_id=int(paciente_id),
            data_internacao=data_internacao,
            hipotese_diagnostica=hipotese
        )
        db.session.add(internacao)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    
    pacientes = Paciente.query.all()
    return render_template('internacao_form.html', pacientes=pacientes)

@bp.route('/<int:id>/alta', methods=['POST'])
def registrar_alta(id):
    internacao = db.session.get(Internacao, id)
    if internacao:
        internacao.data_saida = datetime.today().date()
        db.session.commit()
    return redirect(url_for('main.dashboard'))
