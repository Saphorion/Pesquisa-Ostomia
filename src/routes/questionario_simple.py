from flask import Blueprint, request, jsonify, Response
from src.models.questionario import db, RespostaOstomizado, RespostaProfissional
import json
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

def create_text_report_ostomizado(resposta):
    """Cria um relatório em texto simples para download"""
    report = f"""QUESTIONÁRIO - PESSOA OSTOMIZADA
=====================================

Data de Submissão: {resposta.data_submissao.strftime("%d/%m/%Y %H:%M") if resposta.data_submissao else "N/A"}
ID da Resposta: {resposta.id}

1. PERFIL DO ENTREVISTADO
-------------------------
Nome: {resposta.nome or "Não informado"}
Idade: {resposta.idade or "Não informado"}
Tempo como ostomizado: {resposta.tempo_ostomizado or "Não informado"}
Tipo de ostomia: {resposta.tipo_ostomia or "Não informado"}
Local de acompanhamento médico: {resposta.local_acompanhamento or "Não informado"}
Avaliação do acesso aos insumos: {resposta.avaliacao_acesso or "Não informado"}
Ocupação: {resposta.ocupacao or "Não informado"}
Impacto no trabalho: {resposta.impacto_trabalho or "Não informado"}

2. DESAFIOS NO AUTOCUIDADO
--------------------------
Dificuldades diárias: {resposta.dificuldades_diarias or "Não informado"}
Dificuldades iniciais: {resposta.dificuldades_iniciais or "Não informado"}
Estratégias desenvolvidas: {resposta.estrategias or "Não informado"}
Acesso aos dispositivos: {resposta.acesso_dispositivos or "Não informado"}
Informações desejadas: {resposta.informacoes_desejadas or "Não informado"}

3. SAÚDE FÍSICA E EMOCIONAL
---------------------------
Impacto na autoestima: {resposta.impacto_autoestima or "Não informado"}
Suporte psicológico: {resposta.suporte_psicologico or "Não informado"}
Melhorias no bem-estar: {resposta.melhorias_bem_estar or "Não informado"}

4. ACESSO A SERVIÇOS DE SAÚDE
-----------------------------
Avaliação do atendimento: {resposta.avaliacao_atendimento or "Não informado"}
Barreiras de acesso: {resposta.barreiras_acesso or "Não informado"}
Serviços de orientação: {resposta.servicos_orientacao or "Não informado"}

5. EDUCAÇÃO E INFORMAÇÃO
------------------------
Informação sobre manejo: {resposta.informacao_manejo or "Não informado"}
Informações recebidas: {resposta.informacoes_recebidas or "Não informado"}
Fontes de informação: {resposta.fontes_informacao or "Não informado"}
Avaliação do material: {resposta.avaliacao_material or "Não informado"}
Material educativo: {resposta.material_educativo or "Não informado"}

6. INCLUSÃO E SUPORTE SOCIAL
----------------------------
Reação de familiares: {resposta.reacao_familiares or "Não informado"}
Preconceito enfrentado: {resposta.preconceito or "Não informado"}
Ações de inclusão: {resposta.acoes_inclusao or "Não informado"}

7. DEMANDAS E EXPECTATIVAS
--------------------------
Essencial para qualidade de vida: {resposta.essencial_qualidade_vida or "Não informado"}
Serviços e políticas: {resposta.servicos_politicas or "Não informado"}
Participação em grupos: {resposta.participacao_grupos or "Não informado"}

8. SUSTENTABILIDADE E POLÍTICAS PÚBLICAS
----------------------------------------
Programas municipais: {resposta.programas_municipais or "Não informado"}
Dificuldades de acesso contínuo: {resposta.dificuldades_acesso_continuo or "Não informado"}
Iniciativas governamentais: {resposta.iniciativas_governamentais or "Não informado"}

=====================================
Relatório gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    return report

def create_text_report_profissional(resposta):
    """Cria um relatório em texto simples para download"""
    report = f"""QUESTIONÁRIO - PROFISSIONAL DE SAÚDE
====================================

Data de Submissão: {resposta.data_submissao.strftime("%d/%m/%Y %H:%M") if resposta.data_submissao else "N/A"}
ID da Resposta: {resposta.id}

1. INFORMAÇÕES GERAIS
--------------------
Nome: {resposta.nome or "Não informado"}
Cargo/Função: {resposta.cargo or "Não informado"}
Tempo de experiência: {resposta.tempo_experiencia or "Não informado"}
Instituição: {resposta.instituicao or "Não informado"}

2. PERFIL DO ATENDIMENTO
-----------------------
Frequência de atendimento: {resposta.frequencia_atendimento or "Não informado"}
Especialidades envolvidas: {resposta.especialidades_envolvidas or "Não informado"}
Protocolo específico: {resposta.protocolo_especifico or "Não informado"}

3. DESAFIOS NO ATENDIMENTO
-------------------------
Dificuldades no atendimento: {resposta.dificuldades_atendimento or "Não informado"}
Barreiras aos dispositivos: {resposta.barreiras_dispositivos or "Não informado"}
Questões emocionais: {resposta.questoes_emocionais or "Não informado"}

4. CAPACITAÇÃO E EDUCAÇÃO
------------------------
Treinamento específico: {resposta.treinamento_especifico or "Não informado"}
Materiais educativos: {resposta.materiais_educativos or "Não informado"}
Melhoria na preparação: {resposta.melhoria_preparacao or "Não informado"}

5. POLÍTICAS PÚBLICAS E INFRAESTRUTURA
--------------------------------------
Suporte municipal: {resposta.suporte_municipal or "Não informado"}
Programas de reabilitação: {resposta.programas_reabilitacao or "Não informado"}
Melhorias necessárias: {resposta.melhorias or "Não informado"}

6. INTEGRAÇÃO COM A COMUNIDADE
------------------------------
Aceitação social: {resposta.aceitacao_social or "Não informado"}
Iniciativas de inclusão: {resposta.iniciativas_inclusao or "Não informado"}
Colaboração em projetos: {resposta.colaboracao_projetos or "Não informado"}

====================================
Relatório gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}
"""
    return report

@questionario_bp.route('/admin/download-txt/<tipo>/<int:resposta_id>', methods=['GET'])
def download_text_report(tipo, resposta_id):
    try:
        if tipo == 'ostomizado':
            resposta = RespostaOstomizado.query.get_or_404(resposta_id)
            report_content = create_text_report_ostomizado(resposta)
            filename = f"questionario_ostomizado_{resposta_id}.txt"
        elif tipo == 'profissional':
            resposta = RespostaProfissional.query.get_or_404(resposta_id)
            report_content = create_text_report_profissional(resposta)
            filename = f"questionario_profissional_{resposta_id}.txt"
        else:
            return jsonify({'error': 'Tipo inválido'}), 400
        
        return Response(
            report_content,
            mimetype='text/plain',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

