from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Paciente
from datetime import datetime

bp = Blueprint('pacientes', __name__)

@bp.route('/')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes_list.html', pacientes=pacientes)

@bp.route('/novo', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nasc_str = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        peso = request.form.get('peso')

        data_nascimento = datetime.strptime(data_nasc_str, '%Y-%m-%d').date()

        paciente = Paciente(
            nome=nome,
            data_nascimento=data_nascimento,
            sexo=sexo,
            peso=float(peso) if peso else None,
            cartao_sus=request.form.get('cartao_sus'),
            endereco=request.form.get('endereco'),
            alergias=request.form.get('alergias'),
            comorbidades=request.form.get('comorbidades')
        )
        db.session.add(paciente)
        db.session.commit()
        return redirect(url_for('pacientes.listar_pacientes'))
    
    return render_template('paciente_form.html')
