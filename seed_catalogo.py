from app import create_app, db
from app.models import CatalogoItem

def run_seed():
    app = create_app()
    with app.app_context():
        # Lista padrão de itens básicos de catálogo médico
        itens = [
            "CUIDADOS GERAIS",
            "SINAIS VITAIS, 6/6 H",
            "GLICEMIA CAPILAR, 6/6 H",
            "DIETA LIVRE",
            "ACESSO VENOSO PERIFÉRICO SALINIZADO",
            "CABECEIRA ELEVADA 30°",
            "O2 SE SPO2 < 94%,EM CATETER 3L/MIN",
            "BALANÇO HÍDRICO",
            "DEXMETASONA 1 AMP. + AD EV, 12/12 H",
            "HIDROCORTIZONA 100 MG 1 AMP. + AD EV, 12/12 H",
            "HIDROCORTIZONA 500 MG 1 AMP. + AD EV, 12/12 H",
            "AAS 100 MG 1 CP. VO, APÓS O JANTAR",
            "CLOPIDOGREL 75 MG 1 CP. VO, APÓS O JANTAR",
            "CAPTOPRIL 25 MG 1 CP. VO, 12/12 H",
            "LOSARTANA 50 MG 1 CP. VO, 12/12 H",
            "FUROSEMIDA 2 AMP. EV, 12/12 H",
            "FUROSEMIDA 1 AMP. EV, 8/8 H",
            "NIFEDIPINO 20 MG 1 CP. VO, 12/12 H",
            "HISTAMIN 10 ML VO 8/8 H,",
            "ACEBROFILINA 50MG/5ML 10 ML VO 12/12 H",
            "NBZ: ATROVENT 30 GTT. C/ 3,0 ML SF0,9%, 6/6 H",
            "AEROLIN SPREY 100MCG/DOSE 3 JATOS COM ESPAÇADOR DE 4/4 H",
            "AMINOFILINA 1 AMP. + 100 ML SF0,9% EV, 12/12 H",
            "OMEPRAZOL 40 MG 1 AMP + DILUENTE, ANTES DO CAFÉ",
            "HIDRÓXIDO DE ALUMÍNIO, 20 ML VO DE 8/8 H, SE AZIA",
            "CEFTRIAXONA 1 G, 2 AMP. + 18 ML SF0,9% EV, 24/24 H, D1/D7",
            "METRONIDAZOL 500ML/100ML, 1 BOLSA EV DE 8/8 H, D1/D7",
            "DIPIRONA 1 AMP. + AD EV, 8/8 H, S.N.",
            "BUSCOPAN COMPOSTO 1 AMP. + AD EV, 8/8 H, S.N.",
            "BUSCOPAN SIMPLES 1 AMP. + AD EV, 8/8 H, S.N.",
            "BROMOPRIDA 1 AMP. + AD EV, 8/8 H, S.N.",
            "DICLOFENACO 1 AMP IM, 8/8 H, S.N.",
            "CETOPROFENO 1 AMP. IM 12/12 H, S.N.",
            "PLASIL 1 AMP. IM 8/8 H, S.N.",
            "FLORAX 1 DOSE VO12/12 H, S.N.",
            "TRAMADOL 50MG/ML 1 AMP. + 100 ML SF0,9% EV, 8/8 H, ACM",
            "MORFINA 10MG/ML 1 AMP. + 9 ML AD, APLICAR 3 ML EV, 8/8 H, ACM",
            "GLICOSE 50% 4 AMP. EV, SE DEXTRO < 70 MG/DL",
            "INSULINA REGULAR SC CONFORME GLICEMIA CAPILAR: ATÉ 200: 0",
            "NIFEDIPINO 20 MG 1 CP. VO, SE PA > 160x100 mmHg",
            "CAPTOPRIL 25 MG 1 CP. VO, SE PA > 160x100 mmHg"
        ]
        
        count = 0
        for descricao in itens:
            # Verifica se já existe para evitar duplicidades
            if not CatalogoItem.query.filter_by(descricao_completa=descricao).first():
                novo_item = CatalogoItem(descricao_completa=descricao)
                db.session.add(novo_item)
                count += 1
        
        db.session.commit()
        print(f"Seed concluído: {count} novos itens adicionados ao catálogo.")

if __name__ == '__main__':
    run_seed()
