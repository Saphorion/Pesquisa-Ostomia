from flask import Blueprint, request, jsonify, send_file
from src.models.questionario import db, RespostaOstomizado, RespostaProfissional
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
from datetime import datetime

questionario_bp = Blueprint('questionario', __name__)

@questionario_bp.route('/submit-ostomizados', methods=['POST'])
def submit_ostomizados():
    try:
        data = request.get_json()
        
        resposta = RespostaOstomizado(
            nome=data.get('nome'),
            idade=data.get('idade'),
            tempo_ostomizado=data.get('tempoOstomizado'),
            tipo_ostomia=data.get('tipoOstomia'),
            local_acompanhamento=data.get('localAcompanhamento'),
            avaliacao_acesso=data.get('avaliacaoAcesso'),
            ocupacao=data.get('ocupacao'),
            impacto_trabalho=data.get('impactoTrabalho'),
            dificuldades_diarias=data.get('dificuldadesDiarias'),
            dificuldades_iniciais=data.get('dificuldadesIniciais'),
            estrategias=data.get('estrategias'),
            acesso_dispositivos=data.get('acessoDispositivos'),
            informacoes_desejadas=data.get('informacoesDesejadas'),
            impacto_autoestima=data.get('impactoAutoestima'),
            suporte_psicologico=data.get('suportePsicologico'),
            melhorias_bem_estar=data.get('melhoriasBemEstar'),
            avaliacao_atendimento=data.get('avaliacaoAtendimento'),
            barreiras_acesso=data.get('barreirasAcesso'),
            servicos_orientacao=data.get('servicosOrientacao'),
            informacao_manejo=data.get('informacaoManejo'),
            informacoes_recebidas=data.get('informacoesRecebidas'),
            fontes_informacao=data.get('fontesInformacao'),
            avaliacao_material=data.get('avaliacaoMaterial'),
            material_educativo=data.get('materialEducativo'),
            reacao_familiares=data.get('reacaoFamiliares'),
            preconceito=data.get('preconceito'),
            acoes_inclusao=data.get('acoesInclusao'),
            essencial_qualidade_vida=data.get('essencialQualidadeVida'),
            servicos_politicas=data.get('servicosPoliticas'),
            participacao_grupos=data.get('participacaoGrupos'),
            programas_municipais=data.get('programasMunicipais'),
            dificuldades_acesso_continuo=data.get('dificuldadesAcesso'),
            iniciativas_governamentais=data.get('iniciativasGovernamentais')
        )
        
        db.session.add(resposta)
        db.session.commit()
        
        return jsonify({'success': True, 'id': resposta.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questionario_bp.route('/submit-profissionais', methods=['POST'])
def submit_profissionais():
    try:
        data = request.get_json()
        
        resposta = RespostaProfissional(
            nome=data.get('nome'),
            cargo=data.get('cargo'),
            tempo_experiencia=data.get('tempoExperiencia'),
            instituicao=data.get('instituicao'),
            frequencia_atendimento=data.get('frequenciaAtendimento'),
            especialidades_envolvidas=data.get('especialidadesEnvolvidas'),
            protocolo_especifico=data.get('protocoloEspecifico'),
            dificuldades_atendimento=data.get('dificuldadesAtendimento'),
            barreiras_dispositivos=data.get('barreirasDispositivos'),
            questoes_emocionais=data.get('questoesEmocionais'),
            treinamento_especifico=data.get('treinamentoEspecifico'),
            materiais_educativos=data.get('materiaisEducativos'),
            melhoria_preparacao=data.get('melhoriaPreparacao'),
            suporte_municipal=data.get('suporteMunicipal'),
            programas_reabilitacao=data.get('programasReabilitacao'),
            melhorias=data.get('melhorias'),
            aceitacao_social=data.get('aceitacaoSocial'),
            iniciativas_inclusao=data.get('iniciativasInclusao'),
            colaboracao_projetos=data.get('colaboracaoProjetos')
        )
        
        db.session.add(resposta)
        db.session.commit()
        
        return jsonify({'success': True, 'id': resposta.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questionario_bp.route('/admin/respostas', methods=['GET'])
def get_respostas():
    try:
        tipo = request.args.get('tipo', 'todos')
        
        respostas = []
        
        if tipo in ['todos', 'ostomizados']:
            ostomizados = RespostaOstomizado.query.order_by(RespostaOstomizado.data_submissao.desc()).all()
            for resposta in ostomizados:
                data = resposta.to_dict()
                data['tipo'] = 'ostomizado'
                respostas.append(data)
        
        if tipo in ['todos', 'profissionais']:
            profissionais = RespostaProfissional.query.order_by(RespostaProfissional.data_submissao.desc()).all()
            for resposta in profissionais:
                data = resposta.to_dict()
                data['tipo'] = 'profissional'
                respostas.append(data)
        
        # Ordenar por data de submissão
        respostas.sort(key=lambda x: x['data_submissao'], reverse=True)
        
        return jsonify(respostas), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_pdf_ostomizado(resposta):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    story = []
    
    # Título
    story.append(Paragraph("Questionário - Pessoa Ostomizada", title_style))
    story.append(Spacer(1, 20))
    
    # Informações básicas
    data_formatada = resposta.data_submissao.strftime("%d/%m/%Y %H:%M") if resposta.data_submissao else "N/A"
    story.append(Paragraph(f"<b>Data de Submissão:</b> {data_formatada}", normal_style))
    story.append(Paragraph(f"<b>ID da Resposta:</b> {resposta.id}", normal_style))
    story.append(Spacer(1, 20))
    
    # Seções do questionário
    secoes = [
        ("1. Perfil do Entrevistado", [
            ("Nome", resposta.nome),
            ("Idade", resposta.idade),
            ("Tempo como ostomizado", resposta.tempo_ostomizado),
            ("Tipo de ostomia", resposta.tipo_ostomia),
            ("Local de acompanhamento médico", resposta.local_acompanhamento),
            ("Avaliação do acesso aos insumos", resposta.avaliacao_acesso),
            ("Ocupação", resposta.ocupacao),
            ("Impacto no trabalho", resposta.impacto_trabalho)
        ]),
        ("2. Desafios no Autocuidado", [
            ("Dificuldades diárias", resposta.dificuldades_diarias),
            ("Dificuldades iniciais", resposta.dificuldades_iniciais),
            ("Estratégias desenvolvidas", resposta.estrategias),
            ("Acesso aos dispositivos", resposta.acesso_dispositivos),
            ("Informações desejadas", resposta.informacoes_desejadas)
        ]),
        ("3. Saúde Física e Emocional", [
            ("Impacto na autoestima", resposta.impacto_autoestima),
            ("Suporte psicológico", resposta.suporte_psicologico),
            ("Melhorias no bem-estar", resposta.melhorias_bem_estar)
        ]),
        ("4. Acesso a Serviços de Saúde", [
            ("Avaliação do atendimento", resposta.avaliacao_atendimento),
            ("Barreiras de acesso", resposta.barreiras_acesso),
            ("Serviços de orientação", resposta.servicos_orientacao)
        ]),
        ("5. Educação e Informação", [
            ("Informação sobre manejo", resposta.informacao_manejo),
            ("Informações recebidas", resposta.informacoes_recebidas),
            ("Fontes de informação", resposta.fontes_informacao),
            ("Avaliação do material", resposta.avaliacao_material),
            ("Material educativo", resposta.material_educativo)
        ]),
        ("6. Inclusão e Suporte Social", [
            ("Reação de familiares", resposta.reacao_familiares),
            ("Preconceito enfrentado", resposta.preconceito),
            ("Ações de inclusão", resposta.acoes_inclusao)
        ]),
        ("7. Demandas e Expectativas", [
            ("Essencial para qualidade de vida", resposta.essencial_qualidade_vida),
            ("Serviços e políticas", resposta.servicos_politicas),
            ("Participação em grupos", resposta.participacao_grupos)
        ]),
        ("8. Sustentabilidade e Políticas Públicas", [
            ("Programas municipais", resposta.programas_municipais),
            ("Dificuldades de acesso contínuo", resposta.dificuldades_acesso_continuo),
            ("Iniciativas governamentais", resposta.iniciativas_governamentais)
        ])
    ]
    
    for titulo_secao, campos in secoes:
        story.append(Paragraph(titulo_secao, heading_style))
        
        for label, valor in campos:
            if valor:
                story.append(Paragraph(f"<b>{label}:</b>", normal_style))
                story.append(Paragraph(str(valor), normal_style))
                story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 15))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_pdf_profissional(resposta):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    story = []
    
    # Título
    story.append(Paragraph("Questionário - Profissional de Saúde", title_style))
    story.append(Spacer(1, 20))
    
    # Informações básicas
    data_formatada = resposta.data_submissao.strftime("%d/%m/%Y %H:%M") if resposta.data_submissao else "N/A"
    story.append(Paragraph(f"<b>Data de Submissão:</b> {data_formatada}", normal_style))
    story.append(Paragraph(f"<b>ID da Resposta:</b> {resposta.id}", normal_style))
    story.append(Spacer(1, 20))
    
    # Seções do questionário
    secoes = [
        ("1. Informações Gerais", [
            ("Nome", resposta.nome),
            ("Cargo/Função", resposta.cargo),
            ("Tempo de experiência", resposta.tempo_experiencia),
            ("Instituição", resposta.instituicao)
        ]),
        ("2. Perfil do Atendimento", [
            ("Frequência de atendimento", resposta.frequencia_atendimento),
            ("Especialidades envolvidas", resposta.especialidades_envolvidas),
            ("Protocolo específico", resposta.protocolo_especifico)
        ]),
        ("3. Desafios no Atendimento", [
            ("Dificuldades no atendimento", resposta.dificuldades_atendimento),
            ("Barreiras aos dispositivos", resposta.barreiras_dispositivos),
            ("Questões emocionais", resposta.questoes_emocionais)
        ]),
        ("4. Capacitação e Educação", [
            ("Treinamento específico", resposta.treinamento_especifico),
            ("Materiais educativos", resposta.materiais_educativos),
            ("Melhoria na preparação", resposta.melhoria_preparacao)
        ]),
        ("5. Políticas Públicas e Infraestrutura", [
            ("Suporte municipal", resposta.suporte_municipal),
            ("Programas de reabilitação", resposta.programas_reabilitacao),
            ("Melhorias necessárias", resposta.melhorias)
        ]),
        ("6. Integração com a Comunidade", [
            ("Aceitação social", resposta.aceitacao_social),
            ("Iniciativas de inclusão", resposta.iniciativas_inclusao),
            ("Colaboração em projetos", resposta.colaboracao_projetos)
        ])
    ]
    
    for titulo_secao, campos in secoes:
        story.append(Paragraph(titulo_secao, heading_style))
        
        for label, valor in campos:
            if valor:
                story.append(Paragraph(f"<b>{label}:</b>", normal_style))
                story.append(Paragraph(str(valor), normal_style))
                story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 15))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

@questionario_bp.route('/admin/download-pdf/<tipo>/<int:resposta_id>', methods=['GET'])
def download_pdf(tipo, resposta_id):
    try:
        if tipo == 'ostomizado':
            resposta = RespostaOstomizado.query.get_or_404(resposta_id)
            pdf_buffer = create_pdf_ostomizado(resposta)
            filename = f"questionario_ostomizado_{resposta_id}.pdf"
        elif tipo == 'profissional':
            resposta = RespostaProfissional.query.get_or_404(resposta_id)
            pdf_buffer = create_pdf_profissional(resposta)
            filename = f"questionario_profissional_{resposta_id}.pdf"
        else:
            return jsonify({'error': 'Tipo inválido'}), 400
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

