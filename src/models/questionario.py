from src.models.user import db
from datetime import datetime
import json

class RespostaOstomizado(db.Model):
    __tablename__ = 'respostas_ostomizados'
    
    id = db.Column(db.Integer, primary_key=True)
    data_submissao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Seção 1: Perfil do Entrevistado
    nome = db.Column(db.String(200))
    idade = db.Column(db.String(10))
    tempo_ostomizado = db.Column(db.String(100))
    tipo_ostomia = db.Column(db.String(50))
    local_acompanhamento = db.Column(db.Text)
    avaliacao_acesso = db.Column(db.Text)
    ocupacao = db.Column(db.String(200))
    impacto_trabalho = db.Column(db.Text)
    
    # Seção 2: Desafios no Autocuidado
    dificuldades_diarias = db.Column(db.Text)
    dificuldades_iniciais = db.Column(db.Text)
    estrategias = db.Column(db.Text)
    acesso_dispositivos = db.Column(db.String(100))
    informacoes_desejadas = db.Column(db.Text)
    
    # Seção 3: Saúde Física e Emocional
    impacto_autoestima = db.Column(db.Text)
    suporte_psicologico = db.Column(db.String(100))
    melhorias_bem_estar = db.Column(db.Text)
    
    # Seção 4: Acesso a Serviços de Saúde
    avaliacao_atendimento = db.Column(db.Text)
    barreiras_acesso = db.Column(db.Text)
    servicos_orientacao = db.Column(db.String(100))
    
    # Seção 5: Educação e Informação
    informacao_manejo = db.Column(db.String(100))
    informacoes_recebidas = db.Column(db.Text)
    fontes_informacao = db.Column(db.Text)
    avaliacao_material = db.Column(db.Text)
    material_educativo = db.Column(db.Text)
    
    # Seção 6: Inclusão e Suporte Social
    reacao_familiares = db.Column(db.Text)
    preconceito = db.Column(db.Text)
    acoes_inclusao = db.Column(db.Text)
    
    # Seção 7: Demandas e Expectativas
    essencial_qualidade_vida = db.Column(db.Text)
    servicos_politicas = db.Column(db.Text)
    participacao_grupos = db.Column(db.String(100))
    
    # Seção 8: Sustentabilidade e Políticas Públicas
    programas_municipais = db.Column(db.String(100))
    dificuldades_acesso_continuo = db.Column(db.Text)
    iniciativas_governamentais = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'data_submissao': self.data_submissao.isoformat() if self.data_submissao else None,
            'nome': self.nome,
            'idade': self.idade,
            'tempo_ostomizado': self.tempo_ostomizado,
            'tipo_ostomia': self.tipo_ostomia,
            'local_acompanhamento': self.local_acompanhamento,
            'avaliacao_acesso': self.avaliacao_acesso,
            'ocupacao': self.ocupacao,
            'impacto_trabalho': self.impacto_trabalho,
            'dificuldades_diarias': self.dificuldades_diarias,
            'dificuldades_iniciais': self.dificuldades_iniciais,
            'estrategias': self.estrategias,
            'acesso_dispositivos': self.acesso_dispositivos,
            'informacoes_desejadas': self.informacoes_desejadas,
            'impacto_autoestima': self.impacto_autoestima,
            'suporte_psicologico': self.suporte_psicologico,
            'melhorias_bem_estar': self.melhorias_bem_estar,
            'avaliacao_atendimento': self.avaliacao_atendimento,
            'barreiras_acesso': self.barreiras_acesso,
            'servicos_orientacao': self.servicos_orientacao,
            'informacao_manejo': self.informacao_manejo,
            'informacoes_recebidas': self.informacoes_recebidas,
            'fontes_informacao': self.fontes_informacao,
            'avaliacao_material': self.avaliacao_material,
            'material_educativo': self.material_educativo,
            'reacao_familiares': self.reacao_familiares,
            'preconceito': self.preconceito,
            'acoes_inclusao': self.acoes_inclusao,
            'essencial_qualidade_vida': self.essencial_qualidade_vida,
            'servicos_politicas': self.servicos_politicas,
            'participacao_grupos': self.participacao_grupos,
            'programas_municipais': self.programas_municipais,
            'dificuldades_acesso_continuo': self.dificuldades_acesso_continuo,
            'iniciativas_governamentais': self.iniciativas_governamentais
        }

class RespostaProfissional(db.Model):
    __tablename__ = 'respostas_profissionais'
    
    id = db.Column(db.Integer, primary_key=True)
    data_submissao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Seção 1: Informações Gerais
    nome = db.Column(db.String(200))
    cargo = db.Column(db.String(200))
    tempo_experiencia = db.Column(db.String(100))
    instituicao = db.Column(db.String(200))
    
    # Seção 2: Perfil do Atendimento
    frequencia_atendimento = db.Column(db.String(100))
    especialidades_envolvidas = db.Column(db.Text)
    protocolo_especifico = db.Column(db.String(100))
    
    # Seção 3: Desafios no Atendimento
    dificuldades_atendimento = db.Column(db.Text)
    barreiras_dispositivos = db.Column(db.Text)
    questoes_emocionais = db.Column(db.Text)
    
    # Seção 4: Capacitação e Educação
    treinamento_especifico = db.Column(db.String(100))
    materiais_educativos = db.Column(db.String(100))
    melhoria_preparacao = db.Column(db.Text)
    
    # Seção 5: Políticas Públicas e Infraestrutura
    suporte_municipal = db.Column(db.String(100))
    programas_reabilitacao = db.Column(db.String(100))
    melhorias = db.Column(db.Text)
    
    # Seção 6: Integração com a Comunidade
    aceitacao_social = db.Column(db.Text)
    iniciativas_inclusao = db.Column(db.Text)
    colaboracao_projetos = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'data_submissao': self.data_submissao.isoformat() if self.data_submissao else None,
            'nome': self.nome,
            'cargo': self.cargo,
            'tempo_experiencia': self.tempo_experiencia,
            'instituicao': self.instituicao,
            'frequencia_atendimento': self.frequencia_atendimento,
            'especialidades_envolvidas': self.especialidades_envolvidas,
            'protocolo_especifico': self.protocolo_especifico,
            'dificuldades_atendimento': self.dificuldades_atendimento,
            'barreiras_dispositivos': self.barreiras_dispositivos,
            'questoes_emocionais': self.questoes_emocionais,
            'treinamento_especifico': self.treinamento_especifico,
            'materiais_educativos': self.materiais_educativos,
            'melhoria_preparacao': self.melhoria_preparacao,
            'suporte_municipal': self.suporte_municipal,
            'programas_reabilitacao': self.programas_reabilitacao,
            'melhorias': self.melhorias,
            'aceitacao_social': self.aceitacao_social,
            'iniciativas_inclusao': self.iniciativas_inclusao,
            'colaboracao_projetos': self.colaboracao_projetos
        }

