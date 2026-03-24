from app import create_app, db
from app.models import Paciente, Internacao, CatalogoItem, Prescricao, PrescricaoItens

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Paciente': Paciente, 'Internacao': Internacao, 'CatalogoItem': CatalogoItem, 'Prescricao': Prescricao, 'PrescricaoItens': PrescricaoItens}

if __name__ == '__main__':
    app.run(debug=True)
