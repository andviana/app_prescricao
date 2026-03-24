from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Paciente, Internacao

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    # Listar pacientes "Internados" (sem data de saída)
    internacoes = Internacao.query.filter(Internacao.data_saida.is_(None)).all()
    return render_template('dashboard.html', internacoes=internacoes)
