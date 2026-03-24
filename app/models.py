from datetime import date
from app import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    cartao_sus = db.Column(db.String(20), unique=True, nullable=True)
    sexo = db.Column(db.String(1), nullable=False) # M, F, O
    endereco = db.Column(db.String(255), nullable=True)
    alergias = db.Column(db.Text, nullable=True)
    comorbidades = db.Column(db.Text, nullable=True)
    peso = db.Column(db.Float, nullable=True)

    internacoes = db.relationship('Internacao', back_populates='paciente', cascade='all, delete-orphan')

    @property
    def idade(self):
        today = date.today()
        if not self.data_nascimento:
            return 0
        idade = today.year - self.data_nascimento.year
        if today.month < self.data_nascimento.month or (today.month == self.data_nascimento.month and today.day < self.data_nascimento.day):
            idade -= 1
        return idade

class Internacao(db.Model):
    __tablename__ = 'internacoes'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_internacao = db.Column(db.Date, nullable=False, default=date.today)
    data_saida = db.Column(db.Date, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=db.func.current_timestamp())
    hipotese_diagnostica = db.Column(db.String(255), nullable=True)

    paciente = db.relationship('Paciente', back_populates='internacoes')
    prescricoes = db.relationship('Prescricao', back_populates='internacao', cascade='all, delete-orphan')

    @property
    def dias_internacao(self):
        end_date = self.data_saida if self.data_saida else date.today()
        delta = end_date - self.data_internacao
        return delta.days

    @property
    def tem_prescricao_hoje(self):
        hoje = date.today()
        return any(p.data_prescricao == hoje for p in self.prescricoes)

class CatalogoItem(db.Model):
    __tablename__ = 'catalogo_itens'

    id = db.Column(db.Integer, primary_key=True)
    descricao_completa = db.Column(db.String(255), nullable=False, unique=True)
    # Ex: "DIPIRONA 1 AMP. + AD EV, 8/8 H, S.N."

class Prescricao(db.Model):
    __tablename__ = 'prescricoes'

    id = db.Column(db.Integer, primary_key=True)
    internacao_id = db.Column(db.Integer, db.ForeignKey('internacoes.id'), nullable=False)
    data_prescricao = db.Column(db.Date, nullable=False, default=date.today)
    version_number = db.Column(db.Integer, nullable=False, default=1)
    
    internacao = db.relationship('Internacao', back_populates='prescricoes')
    itens = db.relationship('PrescricaoItens', back_populates='prescricao', cascade='all, delete-orphan')

class PrescricaoItens(db.Model):
    __tablename__ = 'prescricao_itens'

    id = db.Column(db.Integer, primary_key=True)
    prescricao_id = db.Column(db.Integer, db.ForeignKey('prescricoes.id'), nullable=False)
    
    # Salvamos apenas a descrição do item (sem referência ao catálogo)
    descricao_foto = db.Column(db.String(255), nullable=False)

    prescricao = db.relationship('Prescricao', back_populates='itens')
