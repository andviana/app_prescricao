import os
from app import create_app, db
from app.models import Paciente, Internacao, CatalogoItem, Prescricao, PrescricaoItens
from datetime import date
from app.services.pdf_service import gerar_pdf_prescricao

app = create_app()

with app.app_context():
    # Insert Test Patient
    p = Paciente(nome='João Silva', data_nascimento=date(1990, 5, 20), sexo='M', peso=75.5, alergias='Nenhuma', comorbidades='Hipertensão')
    db.session.add(p)
    db.session.commit()

    # Insert Admission
    i = Internacao(paciente_id=p.id, hipotese_diagnostica='Pneumonia')
    db.session.add(i)
    db.session.commit()

    # Insert Items
    c1 = CatalogoItem(descricao_completa='DIPIRONA 1 AMP. + AD EV, 8/8 H, S.N.')
    c2 = CatalogoItem(descricao_completa='CEFTRIAXONA 1G EV 12/12H')
    db.session.add_all([c1, c2])
    db.session.commit()

    # Create Prescription
    presc = Prescricao(internacao_id=i.id)
    db.session.add(presc)
    db.session.flush()

    # Add items to prescription
    pi1 = PrescricaoItens(prescricao_id=presc.id, catalogo_item_id=c1.id, descricao_foto=c1.descricao_completa)
    pi2 = PrescricaoItens(prescricao_id=presc.id, catalogo_item_id=c2.id, descricao_foto=c2.descricao_completa)
    db.session.add_all([pi1, pi2])
    db.session.commit()

    # Generate PDF
    pdf_path = gerar_pdf_prescricao(presc)
    print(f"Success! PDF generated at {pdf_path}")
    
    # Check that age calculation and properties work
    print(f"Idade do paciente: {p.idade} anos")
    print(f"Dias de internação: {i.dias_internacao}")
