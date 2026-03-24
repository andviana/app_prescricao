from fpdf import FPDF
from datetime import date
import tempfile
import os

class PrescricaoPDF(FPDF):
    def __init__(self, prescricao, paciente, internacao):
        super().__init__()
        self.prescricao = prescricao
        self.paciente = paciente
        self.internacao = internacao

    def header(self):
        # Placeholder para logotipo da prefeitura
        # self.image('caminho/para/logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Prefeitura Municipal - Hospital Central', 0, 1, 'C')
        
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Prescrição Médica', 0, 1, 'C')
        self.ln(5)

        # Informações do Paciente
        self.set_font('Arial', '', 10)
        self.cell(100, 6, f'Paciente: {self.paciente.nome}', 0, 0)
        self.cell(45, 6, f'Idade: {self.paciente.idade} anos', 0, 0)
        
        # Omissão de Peso: O campo "Peso" só deve aparecer se o paciente tiver < 16 anos OU < 50kg.
        peso_str = ''
        if self.paciente.peso:
            if self.paciente.idade < 16 or self.paciente.peso < 50.0:
                peso_str = f'Peso: {self.paciente.peso} kg'
        self.cell(45, 6, peso_str, 0, 1)

        self.cell(100, 6, f'DI: {self.internacao.data_internacao.strftime("%d/%m/%Y")} (DIH: {self.internacao.dias_internacao})', 0, 0)
        self.cell(90, 6, f'Data da Prescrição: {self.prescricao.data_prescricao.strftime("%d/%m/%Y")}', 0, 1)

        hd = self.internacao.hipotese_diagnostica if self.internacao.hipotese_diagnostica else 'Não informada'
        self.cell(0, 6, f'HD: {hd}', 0, 1)

        alergias = self.paciente.alergias if self.paciente.alergias else 'Nenhuma relatada'
        self.cell(0, 6, f'Alergias: {alergias}', 0, 1)

        comorbidades = self.paciente.comorbidades if self.paciente.comorbidades else 'Nenhuma relatada'
        self.cell(0, 6, f'Comorbidades: {comorbidades}', 0, 1)
        
        self.ln(5)

        # Cabeçalho da Tabela
        self.set_font('Arial', 'B', 10)
        self.cell(10, 8, 'Nº', 1, 0, 'C')
        self.cell(130, 8, 'Item Prescrito', 1, 0, 'C')
        self.cell(50, 8, 'Horário (Enfermagem)', 1, 1, 'C')

    def footer(self):
        self.set_y(-30)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, f'Versão do Documento: V{self.prescricao.version_number}', 0, 1, 'L')
        
        # Assinaturas
        self.set_y(-25)
        self.set_font('Arial', '', 10)
        self.cell(95, 10, '________________________', 0, 0, 'C')
        self.cell(95, 10, '________________________', 0, 1, 'C')
        self.cell(95, 5, 'Médico (Carimbo e Assinatura)', 0, 0, 'C')
        self.cell(95, 5, 'Enfermeiro(a)', 0, 1, 'C')


def gerar_pdf_prescricao(prescricao):
    internacao = prescricao.internacao
    paciente = internacao.paciente

    pdf = PrescricaoPDF(prescricao, paciente, internacao)
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
        pdf.cell(10, 8, str(idx), 1, 0, 'C')
        
        # Coluna Item (que pode quebrar linha, então calculamos o max Y)
        # Vamos usar um Cell simples limitando o tamanho, ou melhor, truncar para demo
        # Numa aplicação real usaríamos MultiCell e calcularíamos a altura das linhas
        pdf.cell(130, 8, descricao[:80] + ('...' if len(descricao) > 80 else ''), 1, 0, 'L')
        
        # Coluna Horário (em branco para a enfermagem preencher)
        pdf.cell(50, 8, '', 1, 1, 'C')

    # Salva o arquivo em um temporário para retorno
    fd, path = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)
    pdf.output(path)
    return path
