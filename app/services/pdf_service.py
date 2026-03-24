from fpdf import FPDF
from datetime import date
import tempfile
import os
from app.models import Configuracao

class PrescricaoPDF(FPDF):
    def __init__(self, prescricao, paciente, internacao, config=None):
        super().__init__(orientation='L')
        self.set_auto_page_break(auto=True, margin=40)
        self.alias_nb_pages()
        self.prescricao = prescricao
        self.paciente = paciente
        self.internacao = internacao
        self.config = config

    def header(self):
        self.set_font('Arial', 'B', 15)
        
        titulo_empresa = self.config.nome_empresa if self.config and self.config.nome_empresa else 'Prefeitura Municipal - Hospital Central'
        self.cell(0, 10, titulo_empresa, 0, 1, 'C')
        
        # Linha horizontal abaixo do nome da clínica
        current_y = self.get_y()
        self.line(10, current_y, 287, current_y)
        self.ln(2)
            
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Prescrição Médica', 0, 1, 'C')
        self.ln(5)

        # Informações do Paciente
        self.set_font('Arial', '', 10)
        self.cell(150, 6, f'Paciente: {self.paciente.nome}', 0, 0)
        self.cell(60, 6, f'Idade: {self.paciente.idade} anos', 0, 0)
        
        # Omissão de Peso: O campo "Peso" só deve aparecer se o paciente tiver < 16 anos OU < 50kg.
        peso_str = ''
        if self.paciente.peso:
            if self.paciente.idade < 16 or self.paciente.peso < 50.0:
                peso_str = f'Peso: {self.paciente.peso} kg'
        self.cell(60, 6, peso_str, 0, 1)

        self.cell(150, 6, f'DI: {self.internacao.data_internacao.strftime("%d/%m/%Y")} (DIH: {self.internacao.dias_internacao})', 0, 0)
        self.cell(100, 6, f'Data da Prescrição: {self.prescricao.data_prescricao.strftime("%d/%m/%Y")}', 0, 1)

        hd = self.internacao.hipotese_diagnostica if self.internacao.hipotese_diagnostica else 'Não informada'
        self.cell(0, 6, f'HD: {hd}', 0, 1)

        alergias = self.paciente.alergias if self.paciente.alergias else 'Nenhuma relatada'
        self.cell(0, 6, f'Alergias: {alergias}', 0, 1)

        comorbidades = self.paciente.comorbidades if self.paciente.comorbidades else 'Nenhuma relatada'
        self.cell(0, 6, f'Comorbidades: {comorbidades}', 0, 1)
        
        self.ln(5)

        # Cabeçalho da Tabela
        self.set_font('Arial', 'B', 10)
        self.cell(15, 8, 'Nº', 1, 0, 'C')
        self.cell(200, 8, 'Item Prescrito', 1, 0, 'C')
        self.cell(62, 8, 'Horário (Enfermagem)', 1, 1, 'C')

    def footer(self):
        # Assinaturas acima do rodapé
        self.set_y(-35)
        self.set_font('Arial', '', 10)
        self.cell(138, 10, '________________________', 0, 0, 'C')
        self.cell(138, 10, '________________________', 0, 1, 'C')
        self.cell(138, 5, 'Médico (Carimbo e Assinatura)', 0, 0, 'C')
        self.cell(138, 5, 'Enfermeiro(a)', 0, 1, 'C')
        
        # Linha horizontal superior do rodapé
        self.set_y(-16)
        y_line = self.get_y()
        self.line(10, y_line, 287, y_line)
        self.ln(2)
        
        # Dados do rodapé (versão, email, telefone)
        self.set_font('Arial', 'I', 8)
        info_rodape = [f'Versão do Documento: V{self.prescricao.version_number}']
        
        if self.config:
            if self.config.telefone:
                info_rodape.append(f'Tel: {self.config.telefone}')
            if self.config.email:
                info_rodape.append(f'E-mail: {self.config.email}')
                
        y_pos = self.get_y()
        self.cell(0, 5, '  |  '.join(info_rodape), 0, 1, 'C')
        
        self.set_y(y_pos)
        self.cell(0, 5, f'{self.page_no()}/{{nb}}', 0, 0, 'R')


def gerar_pdf_prescricao(prescricao):
    internacao = prescricao.internacao
    paciente = internacao.paciente
    config = Configuracao.query.first()

    pdf = PrescricaoPDF(prescricao, paciente, internacao, config)
    pdf.add_page()
    pdf.set_font('Arial', '', 10)

    # Preencher a tabela de itens prescritos
    for idx, item in enumerate(prescricao.itens, start=1):
        descricao = item.descricao_foto
        # MultiCell não é fácil em tabelas no FPDF1, mas vamos usar um layout simples
        
        # Guardar posição atual
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        # Coluna Nº
        pdf.cell(15, 8, str(idx), 1, 0, 'C')
        
        # Coluna Item (que pode quebrar linha, então calculamos o max Y)
        # Vamos usar um Cell simples limitando o tamanho, ou melhor, truncar para demo
        # Numa aplicação real usaríamos MultiCell e calcularíamos a altura das linhas
        pdf.cell(200, 8, descricao[:120] + ('...' if len(descricao) > 120 else ''), 1, 0, 'L')
        
        # Coluna Horário (em branco para a enfermagem preencher)
        pdf.cell(62, 8, '', 1, 1, 'C')

    # Salva o arquivo em um temporário para retorno
    fd, path = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    pdf.output(path)
    return path
